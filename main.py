# Import the needed libraries
# Date time for tracking what date you first opened it.
# tkinter for GUI support (WIP)
# import random for randint
from datetime import datetime
from tkinter import *
import os, csv, random, hashlib

class Account:
    """ Class account that will register and handle operations of the account management and transaction processing system, as well as record the transactions per account. """
    def __init__(self, accountNumber = None, fName = "", lName = "", initialBal = 0.0, mobileNo = "", email = "", passHash = ""):
        """ Initialize the account with the following details: """
        # if walang intialized account number for some reason, use else and implement random.randint again.
        self.accountNumber = accountNumber if accountNumber else str(random.randint(20210000,20230000))
        self.fName = fName
        self.lName = lName
        self.mobileNo = mobileNo
        self.email = email
        self.balance = float(initialBal)
        self.dateOpened = datetime.now()
        self.transactions = []
        self.status = "Active"
        self.passHash = passHash
        if initialBal < 0:
            raise ValueError("Initial balance cannot be negative")
        elif initialBal > 0:
            self._recordTransaction("Initial Deposit", initialBal)


    def setPassword(self, password):
        """ Password setting for account """
        self.passHash = Password.hashPass(password)
        return True

    def verifyPassword(self, password):
        """ Verify the password """
        if not self.passHash:
            return False
        return Password.verifyPass(password, self.passHash)

    def depositAcc(self,amount):
        """ Deposit money into account """
        if amount <= 0:
            return False, "Deposit amount must be greater than 0"
        if self.status != "Active":
            return False, f"Cannot deposit to {self.status} account"
        self.balance += amount
        self._recordTransaction("Deposit", amount)

        fileHandling.saveTransactions(self.accountNumber, [self.transactions[-1]])
        return True, f"Deposited PHP{amount:.2f}. New balance: PHP{self.balance:.2f}"

    def withdrawAcc(self,amount):
        """ Withdraw money from account """
        if amount <= 0:
            return False, "Withdrawal amount must be greater than 0"
        if self.status != "Active":
            return False, f"Cannot withdraw from {self.status} account"
        if amount > self.balance:
            return False, f"Insufficient funds. Current balance : PHP{self.balance:.2f}"
        
        self.balance -= amount
        self._recordTransaction("Withdrawal", -amount)

        fileHandling.saveTransactions(self.accountNumber, [self.transactions[-1]])
        return True, f"Withdrew PHP{amount:.2f}. New balance: PHP{self.balance:.2f}"

    def _recordTransaction(self, description, amount):
        """ Record the transaction """
        transaction = {
            'date': datetime.now(),
            'description': description,
            'amount': amount,
            'balance': self.balance,
            'accountNumber': self.accountNumber
        }
        self.transactions.append(transaction)

    def getHistory(self):
        """ Get the transaction history of the account based from transactions.csv """
        return self.transactions
    
    def closeAcc(self):
        """ Delete the account from the .csv file but maintain the transactions especially bank transfers. """
        if self.balance > 0:
            return False, "Cannot close account with positive balance."
        self.status = "Closed"
        return True, "Account closed"

    def __str__(self):
        """ String representation of the account """
        return f"Account Number: {self.accountNumber}\nName: {self.fName} {self.lName}\nMobile Number: {self.mobileNo}\nEmail: {self.email}\nBalance: PHP{self.balance:.2f}\nDate Opened: {self.dateOpened}\nStatus: {self.status}"

class Password:
    """ Class for password hashing """

    @staticmethod
    def hashPass(password):
        """ Hash the password using sha256 """

        # create salt so if same password indi siya same hash
        salt = os.urandom(16)
        # create hash object
        hashObj = hashlib.sha256()
        # update the hash object with the salt and password
        hashObj.update(salt)
        # then update the hash object with the password
        # the .encode is to convert the string to bytes
        # then the 'utf-8' is the encoding of the string
        hashObj.update(password.encode('utf-8'))
        # then the .digest() is to return the digest of the data passed to the update() method so that it will return the hash value of the password
        passwordHash = hashObj.digest()
        # then return the salt and password hash in hex format
        return (salt + passwordHash).hex()

    def verifyPass(password,storedHashHex):
        """ Verify the password """
        try:
            #
            storedBytes = bytes.fromhex(storedHashHex)
            
            salt = storedBytes[:16]
            storedHash = storedBytes[16:]
            
            hashObj = hashlib.sha256()
            hashObj.update(salt)
            hashObj.update(password.encode('utf-8'))
            checkHash = hashObj.digest()
            
            return checkHash == storedHash
        except:
            return False

class fileHandling:
    """ File handling of details to .csv files """
    accountFile = "Tam-Bank/userinfo/accounts.csv"
    transactionFile = "Tam-Bank/userinfo/transactions.csv"


    # i used staticmethod so that di na gagamit ng self since di naman needed since ung accountFile and transactionFile is already defined.
    @staticmethod
    def saveFile(accountList):
        """ Save the account details to the .csv file """
        try:
            # with open to open the file, "w" to write, newline to avoid blank lines between rows
            with open(fileHandling.accountFile, "w", newline= '') as csvfile:
                # csv.writer to write the rows
                save = csv.writer(csvfile)
                # write the header row first
                save.writerow(["Account Number", "First Name", "Last Name", "Mobile Number", "Email", "Balance", "Date Opened", "Status", "Password Hash"])

                for account in accountList:
                    # format the date to string so it is consistent.
                    formattedDate = account.dateOpened.strftime('%Y-%m-%d %H:%M:%S')
                    passHash = account.passHash if hasattr(account, 'passHash') else ""
                    save.writerow([account.accountNumber, account.fName, account.lName, account.mobileNo, account.email, account.balance, formattedDate, account.status, passHash])
            
                return True, f"Accounts saved to {fileHandling.accountFile}"
        except Exception as e:
            return False, f"Error saving accounts to {fileHandling.accountFile}: {e}"

    @staticmethod
    def loadFile():
        """ Load the account details from the .csv file """
        # intialize as empty list
        accounts = []

        # if the file does not exist, return the empty list
        if not os.path.exists(fileHandling.accountFile):
            return accounts
        
        # now you know that the file exists, open it
        try:
            with open(fileHandling.accountFile, "r", newline='') as csvfile:
                read = csv.reader(csvfile)
                next(read,None)
                
                # iterate through the rows of data
                for row in read:
                    # if the row has more than 8 columns, process it since the number of columns should be 9 because account number, first name, last name, mobile number, email, balance, date opened, and status.
                    if len(row) >= 8:
                        try:
                            # first initialize the balance to 0.0 to know that it is a float data type
                            initialBal = 0.0
                            # then check if the balance is not empty, then convert it to float and put it in the initialBal variable
                            if row[5]:
                                initialBal = float(row[5])

                            passHash = row[8] if len(row) > 8 else None
                            
                            # now that you have the intialized balance, create an account object with the following details
                            account = Account(
                                accountNumber=row[0], 
                                fName=row[1], 
                                lName=row[2], 
                                initialBal=initialBal,
                                mobileNo=row[3], 
                                email=row[4],
                                passHash=passHash
                            )

                            # now that you have the account object, set the date opened and status
                            date_str = row[6]
                            # try to parse the date string to datetime object, this is so that if the time is not the same format as here, it will not raise an error, because the date will not be the same format as per the other functions requirement.
                            try:
                                account.dateOpened = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                            except ValueError:
                                try:
                                    account.dateOpened = datetime.strptime(date_str, '%Y-%m-%d')
                                except ValueError:
                                    print(f"Warning: Could not parse date '{date_str}', using current time")
                            
                            # set account status based on the row
                            account.status = row[7]
                            account.transactions = fileHandling.loadTransactions(account.accountNumber)
                            accounts.append(account)
                        except Exception as e:
                            print(f"Error processing account row {row}: {e}")
            return accounts
        except Exception as e:
            print(f"Erorr loading accounts : {e}")
            return []
    
    @staticmethod
    def saveTransactions(accountNumber, transactions):
        """ Save the transactions to the .csv file """
        # try to open the file
        try:
            # open the file in append mode, newline to avoid blank lines between rows
            with open(fileHandling.transactionFile, "a", newline='') as csvfile:
                save = csv.writer(csvfile)
                # check if the file is empty, if it is, write the header row
                if csvfile.tell() == 0:
                    save.writerow(["Account Number", "Date", "Description", "Amount", "Balance"])
                # iterate through the transactions in the account object and write them to the file
                for transaction in transactions:
                    accNum = transaction.get('accountNumber', accountNumber)
                    formattedDate = transaction['date'].strftime('%Y-%m-%d %H:%M:%S')
                    save.writerow([accNum, formattedDate, transaction['description'], transaction['amount'], transaction['balance']])
            return True
        except Exception as e:
            print(f"Error saving transactions to {fileHandling.transactionFile}: {e}")
            return False

    @staticmethod
    def loadTransactions(accountNumber):
        """Load transactions for a specific account"""
        # intialize as empty list so that if the path to that file does not exist, it will return an empty list
        transactions = []
        if not os.path.exists(fileHandling.transactionFile):
            return transactions
        
        try:
            # now that you know that the file exists, open it
            with open(fileHandling.transactionFile, 'r', newline='') as csvfile:
                # read the file
                reader = csv.reader(csvfile)
                # skip the header row
                header = next(reader, None)
                # if the header row is empty, return the transactions
                if not header:
                    return transactions
                
                # create column index mapping since dictionary ung gamit
                cols = {name: i for i, name in enumerate(header)}
                accIdx = cols.get("Account Number", 0)
                dateIdx = cols.get("Date", 1)
                descIdx = cols.get("Description", 2)
                amtIdx = cols.get("Amount", 3)
                balIdx = cols.get("Balance", 4)

                # iterate through the rows of the file
                for row in reader:
                    # if the row has more than 5 columns, process it since the number of columns should be 5 because account number, date, description, amount, and balance.
                    if len(row) > accIdx and row[accIdx] == accountNumber:
                        try:
                            date_str = row[dateIdx]
                            try:
                                trans_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
                            except ValueError:
                                trans_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
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

class TamBank:
    """ Manager class for the bank """
    # initialize the accounts as empty dictionary
    # why dictionary? because the account number is unique and it is the key for the dictionary
    # every time you load into the program, it loads the accounts from the file
    # then iterate through the accounts in the accountList and add them in the accounts dictionary
    def __init__(self):
        self.accounts = {}
        accountList = fileHandling.loadFile()
        for account in accountList:
            self.accounts[account.accountNumber] = account
    
    def _loadAccounts(self):
        """ Load the transactions from each account in the .csv file"""
        # load the accounts from the file
        self.accounts = fileHandling.loadFile(self)
        # iterate through the accounts and load the transactions for each account
        for account in self.accounts:
            account.transactions = fileHandling.loadTransactions(account.accountNumber)
        print(f"Loaded {len(self.accounts)} accounts from storage.")
    
    def _saveAccounts(self):
        """ Save the accounts to the .csv file """
        # put the accounts in a list
        accountsList = list(self.accounts.values())
        # save the list to the file
        return fileHandling.saveFile(accountsList)
    
    def createAccount(self, fName = "", lName = "", initialBal = 0.0, mobileNo = "", email = "", password = None):
        """ Create a new account """
        while True:
            accountNumber = str(random.randint(20210000,20230000))
            if accountNumber not in self.accounts:
                break
        account = Account(accountNumber, fName, lName, initialBal, mobileNo, email)

        if password:
            account.setPassword(password)
        
        self.accounts[accountNumber] = account
        self._saveAccounts()
        return account
    
    def authPass(self, accountNumber, password):
        """ Authenticate the password """
        account = self.getAccount(accountNumber)
        if not account:
            return False, "Account not found"
            
        if account.status != "Active":
            return False, "This account is not active"
            
        if not hasattr(account, 'passHash') or not account.passHash:
            return False, "Account has no password set"
            
        if account.verifyPassword(password):
            return True, f"Welcome, {account.fName} {account.lName}"
        else:
            return False, "Invalid password"
    
    def changePass(self, accountNumber, oldPass, newPass):
        """ Change the password """
        success, message = self.authPass(accountNumber, oldPass)
        if not success:
            return False, "Current Password is incorrect"
        
        account = self.getAccount(accountNumber)
        account.setPassword(newPass)
        self._saveAccounts()
        return True, "Password changed successfully"

    def updateAccount(self, fName, lName, mobileNo, email, accountNumber):
        """ Update account details """
        account = self.getAccount(accountNumber)
        if not account:
            return False, "Account not found"
        
        account.fName = fName if fName.strip() else account.fName
        account.lName = lName if lName.strip() else account.lName
        account.mobileNo = mobileNo if mobileNo.strip() else account.mobileNo
        account.email = email if email.strip() else account.email
        
        self._saveAccounts()
        return True, "Account updated successfully"
    
    def deleteAccount(self, accountNumber):
        """ Permanently delete an account from the system """
        if accountNumber not in self.accounts:
            return False, "Account not found"
        
        account = self.accounts[accountNumber]
        if account.balance > 0:
            return False, "Cannot delete account with remaining balance. Please withdraw all funds first."
        
        del self.accounts[accountNumber]
        self._saveAccounts()
        return True, "Account permanently deleted."
    
    def getAccount(self, accountNumber):
        """Get account by account number"""
        return self.accounts.get(accountNumber)
    
    def closeAccount(self, accountNumber):
        """Close an account"""
        account = self.getAccount(accountNumber)
        if not account:
            return False, "Account not found"
            
        success, message = account.closeAcc()
        if success:
            # Update account status in file
            self._saveAccounts()
        
        return success, message
    
    def deposit(self, accountNumber, amount):
        """Deposit to an account"""
        account = self.getAccount(accountNumber)
        if not account:
            return False, "Account not found"
        
        success, message = account.depositAcc(float(amount))
        if success:
            self._saveAccounts()
        
        return success, message
    
    def withdraw(self, accountNumber, amount):
        """Withdraw from an account"""
        account = self.getAccount(accountNumber)
        if not account:
            return False, "Account not found"
        
        success, message = account.withdrawAcc(float(amount))
        if success:
            self._saveAccounts()
        
        return success, message

class LoginMenu:
    """Login and registration menu for TamBank"""
    
    def __init__(self, bank):
        self.bank = bank
    
    def display(self):
        """Display the login menu"""
        print("\n===== TAM BANK =====")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        print("==================")
        
    def run(self):
        """Main menu loop for login interface"""
        while True:
            self.display()
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                self.login()
            elif choice == "2":
                self.register()
            elif choice == "3":
                print("Thank you for using Tam Bank!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def login(self):
        """Handle user login"""
        print("\n===== LOGIN =====")
        accountNumber = input("Account Number: ")
        password = input("Password: ")
        
        success, message = self.bank.authPass(accountNumber, password)
        print(message)
        
        if success:
            user_menu = UserMenu(self.bank, accountNumber)
            user_menu.userMenuRun()
    
    def register(self):
        """Handle new account registration"""
        print("\n===== REGISTER =====")
        fName = input("First Name: ")
        lName = input("Last Name: ")
        
        while True:
            try:
                initialBal = float(input("Initial Balance: "))
                if initialBal < 0:
                    print("Initial balance cannot be negative.")
                    continue
                break
            except ValueError:
                print("Please enter a valid amount.")
        
        mobileNo = input("Mobile Number: ")
        email = input("Email: ")
        

        while True:
            password = input("Password: ")
            confirm = input("Confirm Password: ")
            
            if len(password) < 8:
                print("Password must be at least 8 characters long.")
                continue
                
            if password != confirm:
                print("Passwords do not match.")
                continue
                
            break

        account = self.bank.createAccount(fName, lName, initialBal, mobileNo, email, password)
        
        print(f"\nAccount created successfully!")
        print(f"Your Account Number is: {account.accountNumber}")
        print("Please save this number for future login.")

class UserMenu:
    """ User menu for the bank """
    
    def __init__(self, tamBank, accountNumber):
        """ Constructor which initializes a tambank instance and the current user's account number """
        self.bank = tamBank
        self.accountNumber = accountNumber
        self.account = self.bank.getAccount(accountNumber)
        if not self.account:
            raise ValueError(f"Account {accountNumber} not found")
    
    @staticmethod
    def displayMenu():
        """ Display the main menu """
        print("\n===== TAM-BANK MAIN MENU =====")
        print("1. View Account Details")
        print("2. Update Account Details")
        print("3. View Transaction History")
        print("4. Deposit")
        print("5. Withdraw")
        print("6. Change Password")
        print("7. Close Account")
        print("8. Logout")
        print("===========================")
    
    def userMenuRun(self):
        """ main function to run the user menu """
        while True:
            self.account = self.bank.getAccount(self.accountNumber)
            if not self.account or self.account.status != "Active":
                print("Account not found or closed.")
                break

            self.displayMenu()
            choice = input("Enter choice: ")

            if choice == "1":
                self.viewAccountDetails()
            elif choice == "2":
                self.updateAccountDetails()
            elif choice == "3":
                self.viewTransactionHistory()
            elif choice == "4":
                self.deposit()
            elif choice == "5":
                self.withdraw()
            elif choice == "6":
                self.changePassword()
            elif choice == "7":
                if self.closeAccount():
                    break
            elif choice == "8":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    
    def viewAccountDetails(self):
        """ View account details """
        print("\n===== ACCOUNT DETAILS =====")
        print(self.account)

    def updateAccountDetails(self):
        """Update user's account information"""
        print("\n===== UPDATE ACCOUNT DETAILS =====")
        print("Leave blank to keep current value")
        
        current = self.account
        print(f"Current First Name: {current.fName}")
        fName = input("New First Name: ").strip()
        
        print(f"Current Last Name: {current.lName}")
        lName = input("New Last Name: ").strip()
        
        print(f"Current Mobile Number: {current.mobileNo}")
        mobileNo = input("New Mobile Number: ").strip()
        
        print(f"Current Email: {current.email}")
        email = input("New Email: ").strip()
        
        if any([fName, lName, mobileNo, email]):
            confirm = input("Confirm update? (Y/N): ").lower()
            if confirm == 'y':
                success, message = self.bank.updateAccount(
                    fName, lName, mobileNo, email, self.accountNumber
                )
                print(message)
            else:
                print("Update canceled.")
        else:
            print("No changes made.")
    
    def closeAccount(self):
        """Close the user's account"""
        print("\n===== CLOSE ACCOUNT =====")
        print(f"Current balance: PHP{self.account.balance:.2f}")
        
        if self.account.balance > 0:
            print("You must withdraw all funds before closing the account.")
            withdraw = input("Would you like to withdraw all funds now? (Y/N): ").lower()
            
            if withdraw == 'y':
                success, message = self.bank.withdraw(self.accountNumber, self.account.balance)
                if not success:
                    print(f"Withdrawal failed: {message}")
                    return False
                print(message)
            else:
                print("Account closure canceled.")
                return False
        
        confirm = input("Are you sure you want to close this account? This action cannot be undone. (Y/N): ").lower()
        if confirm != 'y':
            print("Account closure canceled.")
            return False
        
        success, message = self.bank.closeAccount(self.accountNumber)
        print(message)
        
        if success:
            print("Thank you for banking with us.")
            return True
        return False

    def viewAccountStatement(self):
        """Display the users account statement"""
        print("\n===== ACCOUNT STATEMENT =====")
        pass
        
    
            
    def deposit(self):
        """Deposit money into account"""
        print("\n===== DEPOSIT =====")
        try:
            amount = float(input("Enter amount to deposit: PHP"))
            success, message = self.bank.deposit(self.accountNumber, amount)
            print(message)
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    def withdraw(self):
        """Withdraw money from account"""
        print("\n===== WITHDRAW =====")
        try:
            amount = float(input("Enter amount to withdraw: PHP"))
            success, message = self.bank.withdraw(self.accountNumber, amount)
            print(message)
        except ValueError:
            print("Invalid amount. Please enter a number.")
            
    def changePassword(self):
        """Change account password"""
        print("\n===== CHANGE PASSWORD =====")
        current = input("Enter current password: ")
        
        if not self.account.verifyPassword(current):
            print("Current password is incorrect.")
            return
        
        while True:
            new = input("Enter new password: ")
            
            if len(new) < 8:
                print("Password must be at least 8 characters long.")
                continue
                
            confirm = input("Confirm new password: ")
            
            if new != confirm:
                print("New passwords do not match.")
                continue
                
            break
        
        success, message = self.bank.changePass(self.accountNumber, current, new)
        print(message)
    


bank = TamBank()

loginMenu = LoginMenu(bank)
loginMenu.run()