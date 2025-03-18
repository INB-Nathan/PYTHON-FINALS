from models.account import Account
from utils.filehandling import fileHandling
import random

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
