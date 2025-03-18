from datetime import datetime
from utils.password import Password
from utils.filehandling import fileHandling
import random

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

    def depositAcc(self, amount):
        """Delegate to Bank deposit method"""
        from services.bank import Bank 
        bank = Bank()
        return bank.deposit(self.accountNumber, amount)
        
    def withdrawAcc(self, amount):
        """Delegate to Bank withdraw method"""
        from services.bank import Bank
        bank = Bank()
        return bank.withdraw(self.accountNumber, amount)


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
        from services.bank import TamBank
        bank = TamBank()
        return bank.getAccountTransactions(self.accountNumber)
    
    def closeAcc(self):
        """ Delete the account from the .csv file but maintain the transactions especially bank transfers. """
        if self.balance > 0:
            return False, "Cannot close account with positive balance."
        self.status = "Closed"
        return True, "Account closed"

    def __str__(self):
        """ String representation of the account """
        return f"Account Number: {self.accountNumber}\nName: {self.fName} {self.lName}\nMobile Number: {self.mobileNo}\nEmail: {self.email}\nBalance: PHP{self.balance:.2f}\nDate Opened: {self.dateOpened}\nStatus: {self.status}"
