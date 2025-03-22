from datetime import datetime
from utils.password import Password
from utils.filehandling import fileHandling
import random

class Account:
    """ Class account that will register and handle operations of the account management and transaction processing system, as well as record the transactions per account. """
    def __init__(self, accountNumber=None, fName="", lName="", initialBal=0.0, mobileNo="", email="", passHash=None):
        """ Initialize the account with the following details: """
        self.accountNumber = accountNumber if accountNumber else str(random.randint(20210000, 20230000))
        self.fName = fName
        self.lName = lName
        self.mobileNo = mobileNo
        self.email = email
        
        initialBal = float(initialBal) if not isinstance(initialBal, float) else initialBal
        if initialBal < 0:
            raise ValueError("Initial balance cannot be negative")
            
        self.balance = initialBal
        self.dateOpened = datetime.now()
        self.transactions = []
        self.status = "Active"
        self.passHash = passHash
        
        if initialBal > 0:
            self._recordTransaction("Initial Deposit", initialBal)

    def setPassword(self, password):
        """ Password setting for account """
        import hashlib
        self.passHash = hashlib.sha256(password.encode()).hexdigest()
        return True

    def verifyPassword(self, password):
        """Verify the password by direct hash comparison"""
        import hashlib
        
        if not self.passHash:
            return False
            
        attemptHash = hashlib.sha256(password.encode()).hexdigest()
        
        return attemptHash == self.passHash

    def depositAcc(self, amount):
        """Delegate to Bank deposit method"""
        try:
            from services.bank import Bank 
            bank = Bank()
            return bank.deposit(self.accountNumber, amount)
        except ImportError:
            amount = float(amount) if not isinstance(amount, float) else amount
            if amount <= 0:
                return False, "Deposit amount must be greater than 0"
            
            self.balance += amount
            self._recordTransaction("Deposit", amount)
            return True, f"Deposited PHP {amount:.2f}."
        
    def withdrawAcc(self, amount):
        """Delegate to Bank withdraw method"""
        try:
            from services.bank import Bank
            bank = Bank()
            return bank.withdraw(self.accountNumber, amount)
        except ImportError:
            amount = float(amount) if not isinstance(amount, float) else amount
            if amount <= 0:
                return False, "Withdrawal amount must be greater than 0"
                
            if self.balance < amount:
                return False, "Insufficient funds"
                
            self.balance -= amount
            self._recordTransaction("Withdrawal", -amount)
            return True, f"Withdrew PHP {amount:.2f}."

    def _recordTransaction(self, description, amount):
        """ Record the transaction """
        transaction = {
            'date': datetime.now(),
            'description': description,
            'amount': float(amount),
            'balance': self.balance,
            'accountNumber': self.accountNumber
        }
        self.transactions.append(transaction)
        return transaction

    def getHistory(self):
        """ Get the transaction history of the account based from transactions.csv """
        try:
            from services.bank import TamBank
            bank = TamBank()
            return bank.getAccountTransactions(self.accountNumber)
        except ImportError:
            return sorted(self.transactions, key=lambda x: x['date'], reverse=True)
    
    def closeAcc(self):
        """ Delete the account from the .csv file but maintain the transactions especially bank transfers. """
        if self.balance > 0:
            return False, "Cannot close account with positive balance."
        self.status = "Closed"
        return True, "Account closed successfully"

    def __str__(self):
        """ String representation of the account """
        return (f"Account Number: {self.accountNumber}\n"
                f"Name: {self.fName} {self.lName}\n"
                f"Mobile Number: {self.mobileNo}\n"
                f"Email: {self.email}\n"
                f"Balance: PHP{self.balance:.2f}\n"
                f"Date Opened: {self.dateOpened}\n"
                f"Status: {self.status}")