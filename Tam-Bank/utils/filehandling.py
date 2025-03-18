import os
import csv
from datetime import datetime
from models.account import Account

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
