# Import the needed libraries
# Date time for tracking what date you first opened it.
# tkinter for GUI support (WIP)
# import random for randint
from datetime import datetime
from tkinter import *
import random

class Account:
    """ Class account that will register and handle operations of the account management and transaction processing system, as well as record the transactions per account. """
    def __init__(self, accountNumber = None, fName = "", lName = "", initialBal = 0.0, mobileNo = ""):
        self.accountNumber = accountNumber if accountNumber else str(random.randint(20210000,20230000))
        self.fName = fName
        self.lName = lName
        self.mobileNo = mobileNo
        self.balance = float(initialBal)
        self.dateOpened = datetime.now()
        self.transactions = []
        self.status = "Active"
        # Check if initial balance is greater than > 0, so that there is an error catcher if the user inputs a negative value.
        if initialBal > 0:
            try:
                self._recordTransaction("Initial Deposit", initialBal)
                print(f"Initial deposit of ${initialBal:.2f} recorded successfully")
            except Exception as e:
                print(f"Error recording initial deposit: {e}")
                self.balance = 0.0
    
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
