# Import the needed libraries
# Date time for tracking what date you first opened it.
# tkinter for GUI support (WIP)
# import random for randint
from datetime import datetime
from tkinter import *
import os, csv, random

class Account:
    """ Class account that will register and handle operations of the account management and transaction processing system, as well as record the transactions per account. """
    def __init__(self, accountNumber = None, fName = "", lName = "", initialBal = 0.0, mobileNo = "", email = ""):
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
        if initialBal < 0:
            raise ValueError("Initial balance cannot be negative")
        elif initialBal > 0:
            self._recordTransaction("Initial Deposit", initialBal)

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
                save.writerow(["Account Number", "First Name", "Last Name", "Mobile Number", "Email", "Balance", "Date Opened", "Status"])

                for account in accountList:
                    # format the date to string so it is consistent.
                    formattedDate = account.dateOpened.strftime('%Y-%m-%d %H:%M:%S')
                    save.writerow([account.accountNumber, account.fName, account.lName, account.mobileNo, account.email, account.balance, formattedDate, account.status])
            
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
                            
                            # now that you have the intialized balance, create an account object with the following details
                            account = Account(
                                accountNumber=row[0], 
                                fName=row[1], 
                                lName=row[2], 
                                initialBal=initialBal,
                                mobileNo=row[3], 
                                email=row[4]
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
    
    def createAccount(self, fName = "", lName = "", initialBal = 0.0, mobileNo = "", email = ""):
        """ Create a new account """
        while True:
            accountNumber = str(random.randint(20210000,20230000))
            if accountNumber not in self.accounts:
                break
        account = Account(accountNumber, fName, lName, initialBal, mobileNo, email)
        self.accounts[accountNumber] = account
        self._saveAccounts()
        return account
    
    def getAccount(self, account_number):
        """Get account by account number"""
        return self.accounts.get(account_number)
    
    def closeAccount(self, account_number):
        """Close an account"""
        account = self.get_account(account_number)
        if not account:
            return False, "Account not found"
            
        success, message = account.closeAcc()
        if success:
            # Update account status in file
            self._saveAccounts()
        
        return success, message
    
    def deposit(self, account_number, amount):
        """Deposit to an account"""
        account = self.getAccount(account_number)
        if not account:
            return False, "Account not found"
        
        success, message = account.depositAcc(float(amount))
        if success:
            self._saveAccounts()
        
        return success, message
    
    def withdraw(self, account_number, amount):
        """Withdraw from an account"""
        account = self.getAccount(account_number)
        if not account:
            return False, "Account not found"
        
        success, message = account.withdrawAcc(float(amount))
        if success:
            self._saveAccounts()
        
        return success, message

print("===== FILE HANDLING TEST =====\n")


bank = TamBank()

account1 = bank.createAccount("Camama", "Earl", 1020.0, "09123426789")
print(f"Created: {account1}")

account2 = bank.createAccount("Borja", "Fernando Dane", 5020.0, "09876143210")
print(f"Created: {account2}")

account3 = bank.createAccount("Cabrales", "Nathan Josua", 2050.0, "09123426724")
print(f"Created: {account1}")

account4 = bank.createAccount("Tendero", "Guinevere", 500.0, "09876143111")
print(f"Created: {account2}")

print("\nPerforming transactions...")
status1, msg1 = bank.deposit(account1.accountNumber, 250)
print(f"Deposit: {msg1}")

status2, msg2 = bank.withdraw(account1.accountNumber, 100)
print(f"Withdrawal: {msg2}")

status3, msg3 = bank.deposit(account2.accountNumber, 300)
print(f"Deposit: {msg3}")

status4, msg4 = bank.withdraw(account2.accountNumber, 200)
print(f"Withdrawal: {msg4}")

status5, msg5 = bank.deposit(account3.accountNumber, -100)
print(f"Deposit: {msg5}")

status6, msg6 = bank.withdraw(account3.accountNumber, 2050.50)
print(f"Withdrawal: {msg6}")

status7, msg7 = bank.deposit(account4.accountNumber, 12043.2323123)
print(f"Deposit: {msg7}")

print("\nUpdated accounts:")
print(bank.getAccount(account1.accountNumber))
print()
print(bank.getAccount(account2.accountNumber))
print()
print(bank.getAccount(account3.accountNumber))
print()
print(bank.getAccount(account4.accountNumber))


bank = None 

new_bank = TamBank()

print("\nAccounts after reloading:")
if account1.accountNumber in new_bank.accounts:
    print(new_bank.getAccount(account1.accountNumber))
else:
    print(f"Account {account1.accountNumber} not found after reload!")

print()

if account2.accountNumber in new_bank.accounts:
    print(new_bank.getAccount(account2.accountNumber))
else:
    print(f"Account {account2.accountNumber} not found after reload!")

print()

if account3.accountNumber in new_bank.accounts:
    print(new_bank.getAccount(account3.accountNumber))
else:
    print(f"Account {account3.accountNumber} not found after reload!")

print()

if account4.accountNumber in new_bank.accounts:
    print(new_bank.getAccount(account4.accountNumber))
else:
    print(f"Account {account4.accountNumber} not found after reload!")

print()

print("\n===== TEST COMPLETED =====")

