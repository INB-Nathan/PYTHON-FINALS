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
        self.accountNumber = accountNumber if accountNumber else str(random.randint(20210000,20230000))
        self.fName = fName
        self.lName = lName
        self.mobileNo = mobileNo
        self.email = email
        self.balance = float(initialBal)
        self.dateOpened = datetime.now()
        self.transactions = []
        self.status = "Active"
        # Check if initial balance is greater than > 0, so that there is an error catcher if the user inputs a negative value.
        if initialBal < 0:
            raise ValueError("Initial balance cannot be negative")
        elif initialBal > 0:
            self._recordTransaction("Initial Deposit", initialBal)

    def depositAcc(self,amount):
        """ deposit nga ni eh """
        pass

    def withdrawAcc(self,amount):
        """ withdraw nga ni eh """
        pass

    def _recordTransaction(self, description, amount):
        """ record man daw ng transaksyon"""
        pass

    def getHistory(self):
        """ This function will return the history of transactions which is stored in transactions. """
        return self.transactions
    
    def closeAcc(self):
        """ Delete the account from the .csv file but maintain the transactions especially bank transfers. """
        if self.balance > 0:
            return False, "Cannot close account with positive balance."
        self.status = "Closed"
        return True, "Account closed"
    
    def __str__(self):
        """ Returns a string representation of the Account object """
        account_status = "Active" if self.status == "Active" else f"[{self.status}]"
        formatted_date = self.dateOpened.strftime('%Y-%m-%d %H:%M:%S')
        
        return (f"Account #{self.accountNumber} - {self.fName} {self.lName}: ${self.balance:.2f}\n"
                f"Status: {account_status}\n"
                f"Mobile: {self.mobileNo}\n"
                f"Opened: {formatted_date}")

class fileHandling:
    """ File handling of details to .csv files """
    accountFile = "accounts.csv"
    transactionFile = "transactions.csv"

    def saveFile(self):
        """ Save the account details to the .csv file """
        try:
            with open(self.accountFile, "w", newline= '') as csvfile:
                save = csv.writer(csvfile)
                save.writerow(["Account Number", "First Name", "Last Name", "Mobile Number", "Email", "Balance", "Date Opened", "Status"])

                for account in self.accounts:
                    save.writerow([account.accountNumber, account.fName, account.lName, account.mobileNo, account.email, account.balance, account.dateOpened, account.status])
            
                return True, f"Accounts saved to {self.accountFile}"
        except Exception as e:
            return False, f"Error saving accounts to {self.accountFile}: {e}"


    def loadFile(self):
        """ Load the account details from the .csv file """
        accounts = []

        if not os.path.exists(self.accountFile):
            return accounts
        
        try:
            with open(self.accountFile, "r", newline='') as csvfile:
                read = csv.reader(csvfile)
                
                for row in read:
                    account = Account(accountNumber=row[0], fName=row[1], lName=row[2], mobileNo=row[3], email=row[4], initialBal=row[5])
                    account.dateOpened = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
                    account.status = row['Status']

                    account.transactions = self.loadTransactions(account.accountNumber)
                    accounts.append(account)
            return accounts
        except Exception as e:
            print(f"Erorr loading accounts : {e}")
            return []
    
    def saveTransactions(self, accountNumber):
        """ Save the transactions to the .csv file """
        try:
            with open(self.transactionFile, "a", newline='') as csvfile:
                save = csv.writer(csvfile)
                if csvfile.tell() == 0:
                    save.writerow(["Account Number", "Date", "Description", "Amount", "Balance"])
                for transaction in self.transactions:
                    save.writerow([transaction['accountNumber'], transaction['date'], transaction['description'], transaction['amount'], transaction['balance']])
            return True
        except Exception as e:
            print(f"Error saving transactions to {self.transactionFile}: {e}")
            return False

    def loadTransactions(self, accountNumber):
        """Load transactions for a specific account"""
        transactions = []
        
        if not os.path.exists(self.transactionFile):
            return transactions
        
        try:
            with open(self.transactionFile, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    if row['AccountNumber'] == accountNumber:
                        transaction = {
                            'date': datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S'),
                            'description': row['Description'],
                            'amount': float(row['Amount']),
                            'balance': float(row['BalanceAfter'])
                        }
                        transactions.append(transaction)
            
            return transactions
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return []
