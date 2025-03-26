import os
import csv
from datetime import datetime

class FileHandling:
    """ File handling of details to .csv files with enhanced account type storage """
    applicationFile = "Tam-Bank/userinfo/applications.csv"
    accountFile = "Tam-Bank/userinfo/accounts.csv"
    transactionFile = "Tam-Bank/userinfo/transactions.csv"
    
    # Minimum balance constant to enforce requirements
    MIN_BALANCE = 50.0  # Set this to your actual minimum balance requirement

    @staticmethod
    def saveFile(accountList):
        """ Save the account details to the .csv file with account type """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(FileHandling.accountFile), exist_ok=True)
            
            with open(FileHandling.accountFile, "w", newline='') as csvfile:
                save = csv.writer(csvfile)
                # Modified header to include Account Type
                save.writerow([
                    "Account Number", "First Name", "Last Name", "Mobile Number", 
                    "Email", "Balance", "Date Opened", "Status", "Password Hash", "Account Type"
                ])

                for account in accountList:
                    # Format the date to string for consistency
                    formattedDate = account.dateOpened.strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Handle optional attributes with defensive programming
                    passHash = account.passHash if hasattr(account, 'passHash') else ""
                    
                    # Get account type with fallback to "Savings" if not present
                    accountType = getattr(account, 'accountType', "Savings")
                    
                    # Write row with account type
                    save.writerow([
                        account.accountNumber, account.fName, account.lName, 
                        account.mobileNo, account.email, account.balance, 
                        formattedDate, account.status, passHash, accountType
                    ])
            
            return True, f"Accounts saved to {FileHandling.accountFile}"
        except Exception as e:
            return False, f"Error saving accounts to {FileHandling.accountFile}: {e}"

    @staticmethod
    def loadFile():
        """ Load the account details from the .csv file with account type """
        from models.account import Account
        accounts = []

        # Return empty list if file doesn't exist
        if not os.path.exists(FileHandling.accountFile):
            return accounts
        
        try:
            with open(FileHandling.accountFile, "r", newline='') as csvfile:
                read = csv.reader(csvfile)
                header = next(read, None)
                
                # Map column indices for flexibility and backward compatibility
                col_indices = {}
                for i, col_name in enumerate(header or []):
                    col_indices[col_name] = i
                
                # Iterate through the rows of data
                for row in read:
                    # Skip processing if row is too short
                    if len(row) < 8:
                        continue
                        
                    try:
                        # Initialize balance with proper error handling
                        initialBal = 0.0
                        try:
                            if row[5]:
                                initialBal = float(row[5])
                        except (ValueError, IndexError):
                            pass

                        # Extract password hash if available
                        passHash = row[8] if len(row) > 8 else None
                        
                        # Extract account type if available (backward compatibility)
                        accountType = "Savings"  # Default value
                        type_index = col_indices.get("Account Type")
                        if type_index is not None and len(row) > type_index:
                            accountType = row[type_index] or "Savings"
                        
                        # Create account object
                        account = Account(
                            accountNumber=row[0], 
                            fName=row[1], 
                            lName=row[2], 
                            initialBal=initialBal,
                            mobileNo=row[3], 
                            email=row[4],
                            passHash=passHash
                        )
                        
                        # Set account type
                        account.accountType = accountType

                        # Parse date with robust error handling
                        date_str = row[6]
                        try:
                            account.dateOpened = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            try:
                                account.dateOpened = datetime.strptime(date_str, '%Y-%m-%d')
                            except ValueError:
                                # Fallback to current time if date parsing fails
                                account.dateOpened = datetime.now()
                                print(f"Warning: Could not parse date '{date_str}', using current time")
                        
                        # Set account status
                        account.status = row[7]
                        
                        # Load transactions
                        account.transactions = FileHandling.loadTransactions(account.accountNumber)
                        
                        # Add to accounts list
                        accounts.append(account)
                    except Exception as e:
                        print(f"Error processing account row {row}: {e}")
            return accounts
        except Exception as e:
            print(f"Error loading accounts: {e}")
            return []
    
    @staticmethod
    def saveTransactions(accountNumber, transactions):
        """ Save the transactions to the .csv file """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(FileHandling.transactionFile), exist_ok=True)
            
            # Check if file exists
            file_exists = os.path.exists(FileHandling.transactionFile) and os.path.getsize(FileHandling.transactionFile) > 0
            
            with open(FileHandling.transactionFile, "a", newline='') as csvfile:
                save = csv.writer(csvfile)
                if not file_exists:
                    save.writerow(["Account Number", "Date", "Description", "Amount", "Balance"])
                
                for transaction in transactions:
                    accNum = transaction.get('accountNumber', accountNumber)
                    formattedDate = transaction['date'].strftime('%Y-%m-%d %H:%M:%S')
                    save.writerow([accNum, formattedDate, transaction['description'], 
                                  transaction['amount'], transaction['balance']])
            return True
        except Exception as e:
            print(f"Error saving transactions to {FileHandling.transactionFile}: {e}")
            return False

    @staticmethod
    def loadTransactions(accountNumber):
        """Load transactions for a specific account"""
        transactions = []
        if not os.path.exists(FileHandling.transactionFile):
            return transactions
        
        try:
            with open(FileHandling.transactionFile, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader, None)
                if not header:
                    return transactions
                
                # Dynamic column mapping for flexibility
                cols = {name: i for i, name in enumerate(header)}
                accIdx = cols.get("Account Number", 0)
                dateIdx = cols.get("Date", 1)
                descIdx = cols.get("Description", 2)
                amtIdx = cols.get("Amount", 3)
                balIdx = cols.get("Balance", 4)

                for row in reader:
                    # Skip processing if row is too short
                    if len(row) <= max(accIdx, dateIdx, descIdx, amtIdx, balIdx):
                        continue
                        
                    # Only process transactions for the specified account
                    if row[accIdx] == accountNumber:
                        try:
                            # Parse date with robust error handling
                            date_str = row[dateIdx]
                            try:
                                trans_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
                            except ValueError:
                                try:
                                    trans_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                                except ValueError:
                                    # Fallback to current time
                                    trans_date = datetime.now()
                            
                            # Construct transaction dictionary
                            transaction = {
                                'date': trans_date,
                                'description': row[descIdx],
                                'amount': float(row[amtIdx]),
                                'balance': float(row[balIdx]),
                                'accountNumber': accountNumber
                            }
                            transactions.append(transaction)
                        except Exception as e:
                            print(f"Error processing transaction row {row}: {e}")
            return transactions
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return []
    
    @staticmethod
    def saveApplication(fName, lName, mobileNo, email, initialBal, bankType):
        """Save a new application to the applications.csv file"""
        try:
            # Validate minimum balance requirement before proceeding
            initialBal = float(initialBal) if isinstance(initialBal, str) else initialBal
            if initialBal < FileHandling.MIN_BALANCE:
                return False, f"Initial balance must be at least ${FileHandling.MIN_BALANCE:.2f}"
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(FileHandling.applicationFile), exist_ok=True)
            
            # Check if file exists and write header if needed
            file_exists = os.path.exists(FileHandling.applicationFile) and os.path.getsize(FileHandling.applicationFile) > 0
            
            with open(FileHandling.applicationFile, "a", newline='') as csvfile:
                save = csv.writer(csvfile)
                
                # Write header if file is new or empty
                if not file_exists:
                    save.writerow([
                        "Application ID", "First Name", "Last Name", "Mobile Number", 
                        "Email", "Initial Balance", "Bank Type", "Status", "Application Date"
                    ])
                
                # Generate unique application ID
                applicationId = f"APP-{int(datetime.now().timestamp())}"
                applicationDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Write application data
                save.writerow([
                    applicationId, fName, lName, mobileNo, email, initialBal, 
                    bankType, "Pending", applicationDate
                ])
                
            return True, applicationId
        except Exception as e:
            return False, f"Error saving application: {e}"
        
    @staticmethod
    def loadApplications(status=None):
        """Load all applications or filter by status"""
        applications = []
        
        if not os.path.exists(FileHandling.applicationFile):
            return applications
        
        try:
            with open(FileHandling.applicationFile, "r", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    # Filter by status if specified
                    if status and row['Status'] != status:
                        continue
                        
                    # Convert initial balance to float with error handling
                    try:
                        initialBal = float(row['Initial Balance']) if row['Initial Balance'] else 0.0
                    except ValueError:
                        initialBal = 0.0
                        
                    # Parse application date with error handling
                    try:
                        appDate = datetime.strptime(row['Application Date'], '%Y-%m-%d %H:%M:%S')
                    except (ValueError, KeyError):
                        appDate = datetime.now()
                        
                    # Create application dictionary
                    application = {
                        'applicationId': row['Application ID'],
                        'fName': row['First Name'],
                        'lName': row['Last Name'],
                        'mobileNo': row['Mobile Number'],
                        'email': row['Email'],
                        'initialBal': initialBal,
                        'bankType': row.get('Bank Type', 'Savings'),  # Use default if missing
                        'status': row['Status'],
                        'applicationDate': appDate
                    }
                    
                    applications.append(application)
                    
            return applications
        except Exception as e:
            print(f"Error loading applications: {e}")
            return []
    
    @staticmethod
    def updateApplicationStatus(applicationId, newStatus):
        """Update the status of an application (Pending, Accepted, Declined)"""
        # Input validation
        if not applicationId:
            return False, "Invalid application ID"
            
        if newStatus not in ["Pending", "Accepted", "Declined"]:
            return False, "Invalid status. Must be Pending, Accepted, or Declined."
            
        if not os.path.exists(FileHandling.applicationFile):
            return False, "Applications file does not exist"
            
        try:
            # Read all applications
            applications = []
            updated = False
            
            with open(FileHandling.applicationFile, "r", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                headers = reader.fieldnames
                
                for row in reader:
                    if row['Application ID'] == applicationId:
                        row['Status'] = newStatus
                        updated = True
                    applications.append(row)
                    
            if not updated:
                return False, f"Application with ID {applicationId} not found"
                
            # Write back to file
            with open(FileHandling.applicationFile, "w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(applications)
                
            return True, f"Application {applicationId} status updated to {newStatus}"
        except Exception as e:
            return False, f"Error updating application status: {e}"