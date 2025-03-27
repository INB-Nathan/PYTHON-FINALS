# import needed dependencies or modules.
from models.account import Account
from utils.filehandling import FileHandling
from datetime import datetime, timedelta
import random, csv, os, hashlib

class TamBank:
    """ Manager class for the bank """
    def __init__(self):
        self.accounts = {}
        accountList = FileHandling.loadFile()
        for account in accountList:
            self.accounts[account.accountNumber] = account
    
    def _loadAccounts(self):
        """ Load the transactions from each account in the .csv file"""
        # load the accounts from the .csv file
        self.accounts = FileHandling.loadFile(self)
        # for loop to load the transactions from each account
        for account in self.accounts:
            account.transactions = FileHandling.loadTransactions(account.accountNumber)
        return len(self.accounts)
    
    def _saveAccounts(self):
        """ Save the accounts to the .csv file """
        # save the accounts to the .csv file
        accountsList = list(self.accounts.values())
        return FileHandling.saveFile(accountsList)
    
    def createAccount(self, fName="", lName="", initialBal=0.0, mobileNo="", email="", password=None):
        """ Create a new account """
        while True:
            accountNumber = str(random.randint(20210000, 20230000))
            if accountNumber not in self.accounts:
                break
        account = Account(accountNumber, fName, lName, initialBal, mobileNo, email)

        if password:
            account.setPassword(password)
        
        self.accounts[accountNumber] = account
        self._saveAccounts()
        return account

    def _checkAccountStatus(self, accountNumber):
        """ Check if the account has been inactive for 3 months and update the status """
        from datetime import datetime, timedelta
        
        account = self.getAccount(accountNumber)
        if not account or account.status.lower() != "active":
            return False
        
        transactions = self.getAccountTransactions(accountNumber)
        
        if not transactions:
            lastActivityDate = account.dateOpened
        else:
            lastActivityDate = max(transaction['date'] for transaction in transactions)
        
        current_date = datetime.now()
        threeMonthsAgo = current_date - timedelta(days=90)
        
        if lastActivityDate < threeMonthsAgo:
            account.status = "Inactive"
            
            description = f"Account status changed to Inactive due to 3 months of inactivity"
            self._saveTransaction(accountNumber, "SYSTEM", 0.0, description)
            
            self._saveAccounts()
            
            return True
        
        return False
    
    def reactivateAccount(self,accountNumber):
        """ reactivates an account when there is activity not just logging in. """

        account = self.getAccount(accountNumber)
        if not account:
            return False, "Account not found"
        
        if account.status.lower() != "inactive":
            return False, f"Account is not inactive. Current status: {account.status}"
        
        account.status = "Active"
        
        description = "Account reactivated"
        self._saveTransaction(accountNumber, "SYSTEM", 0.0, description)
        
        self._saveAccounts()
        
        return True, "Account successfully reactivated"
    
    def authPass(self, accountNumber, password):
        """ Authenticate the password with debugging """
        import hashlib
        
        account = self.getAccount(accountNumber)
        if not account:
            return False, "Account not found"
        
        if not self.isAdmin(accountNumber):
            self._checkAccountStatus(accountNumber)
        
            account = self.getAccount(accountNumber)

                
        if account.status.lower() not in ["active", "inactive"]:
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
        if not account:
            return False, "Account not found"
        
        import hashlib
        newHash = hashlib.sha256(newPass.encode()).hexdigest()
        account.passHash = newHash

        self._saveAccounts()
        verifySucess, _ = self.authPass(accountNumber, newPass)
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
            self._saveAccounts()
        
        return success, message
    
    def deposit(self, accountNumber, amount):
        """Deposit to an account"""
        account = self.getAccount(accountNumber)
        if not account:
            return False, "Account not found"
        
        status_valid, status_message = self._validateAccountStatus(account, "deposit")
        if not status_valid:
            return False, status_message
        
        amount = float(amount) if not isinstance(amount, float) else amount

        

        if float(amount) <= 0:
            return False, "Deposit amount must be greater than 0"
        
        account.balance += amount

        self._saveTransaction(accountNumber, accountNumber, amount, "Deposit")
        self._saveAccounts()

        return True, f"Deposited PHP {amount:.2f}."
    
    def withdraw(self, accountNumber, amount):
        """Withdraw from an account"""
        account = self.getAccount(accountNumber)
        if not account:
            return False, "Account not found"
        
        status_valid, status_message = self._validateAccountStatus(account, "withdrawal")
        if not status_valid:
            return False, status_message
        
        amount = float(amount) if not isinstance(amount, float) else amount

        if amount <= 0:
            return False, "Withdrawal amount must be greater than 0"
        
        if account.balance < amount:
            return False, "Insufficient funds"
        
        account.balance -= amount

        self._saveTransaction(accountNumber, "CASH", amount, "Withdrawal")
        self._saveAccounts()

        return True, f"Withdrawed PHP {float(amount):.2f}."
    
    def transaction(self, accountNumber, toAccount, amount, description):
        """Transfer between accounts"""
        fromAccount = self.getAccount(accountNumber)
        if not fromAccount:
            return False, "Sender account not found"
        
        toAccount = self.getAccount(toAccount)
        if not toAccount:
            return False, "Recipient account not found"
        
        status_valid, status_message = self._validateAccountStatus(fromAccount, "transfer")
        if not status_valid:
            return False, status_message
        
        status_valid, status_message = self._validateAccountStatus(toAccount, "transfer")
        if not status_valid:
            return False, status_message

        
        amount = float(amount)
        if fromAccount.balance < amount:
            return False, "Insufficient funds"
        
        fromAccount.balance -= amount
        toAccount.balance += amount
        
        self._saveTransaction(accountNumber, toAccount, amount, description)
        self._saveAccounts()
        
        return True, f"Successfully transferred PHP {amount:.2f} to account {toAccount.accountNumber}"
    
    def _saveTransaction(self, fromAccount, toAccount, amount, description):
        """ Save transactions to transactions.csv"""
        transacPath = "Tam-Bank/userinfo/transactions.csv"
        transacId = self._generateTransacId()
        currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        fileExists = os.path.isfile(transacPath) and os.path.getsize(transacPath) > 0
        with open(transacPath, 'a', newline='') as file:
            writer = csv.writer(file)
            if not fileExists:
                writer.writerow(['transacId', 'date', 'from_account', 'to_account', 'amount', 'description'])
            
            writer.writerow([transacId, currentDate, fromAccount, toAccount, amount, description])
    
    def _generateTransacId(self):
        """ Generate a unique transaction ID """
        return random.randint(100000, 999999)
    
    def getAccountTransactions(self, accountNumber):
        """ Get all transactions for an account """
        transacPath = "Tam-Bank/userinfo/transactions.csv"
        transactions = []
        
        try:
            with open(transacPath, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['from_account'] == accountNumber or row['to_account'] == accountNumber:
                        try:
                            amount = float(row['amount'])
                            if row["from_account"] == accountNumber and row["from_account"] != row["to_account"]:
                                amount = -amount
                                
                            try:
                                date_obj = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                            except ValueError:
                                date_obj = datetime.now()
                                
                            transactions.append({ 
                                "date": date_obj,
                                "description": row['description'],
                                "amount": amount,
                                "transacId": row['transacId']
                            })
                        except Exception:
                            continue
        except Exception:
            pass

        transactions.sort(key=lambda x: x['date'], reverse=True)
        return transactions
    
    def getAllAccounts(self):
        """Get all accounts in the system and update the accounts dictionary"""
        accounts = []
        
        try:
            with open('Tam-Bank/userinfo/accounts.csv', 'r') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        account_number = row['Account Number']
                        
                        account = Account(
                            account_number,
                            row['First Name'],
                            row['Last Name'],
                            float(row['Balance']),
                            row['Mobile Number'],
                            row['Email'],
                            row.get('Password Hash', None)
                        )
                        
                        try:
                            account.dateOpened = datetime.strptime(row['Date Opened'], '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            account.dateOpened = datetime.now()
                            
                        account.status = row['Status'] if 'Status' in row else "Active"
                        
                        self.accounts[account_number] = account
                        
                        accounts.append(account)
                        
                    except Exception:
                        continue
                        
        except Exception:
            pass
            
        return accounts

    def getAccountPasswordHash(self, account_number):
        """Get the password hash for a specific account"""
        if hasattr(self, 'account_password_hashes') and account_number in self.account_password_hashes:
            return self.account_password_hashes[account_number]
        return None

    def adminUpdateAccount(self, originalId, newId, fname, lname, mobile, email, status, password=None):
        """Update account details with admin privileges (no validation)"""
        import csv
        import os
        
        accountsData = []
        found = False
        
        try:
            with open('Tam-Bank/userinfo/accounts.csv', 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                
                for row in reader:
                    if row['Account Number'] == originalId:
                        found = True
                        row['Account Number'] = newId
                        row['First Name'] = fname
                        row['Last Name'] = lname
                        row['Mobile Number'] = mobile
                        row['Email'] = email
                        row['Status'] = status
                    
                    accountsData.append(row)
            
            if not found:
                return False
            
            with open('Tam-Bank/userinfo/accounts.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(accountsData)
            
            if password and len(password) > 0:
                import hashlib
                passHash = hashlib.sha256(password.encode()).hexdigest()
                
                with open('Tam-Bank/userinfo/accounts.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    fieldnames = reader.fieldnames
                    rows = list(reader)
                    
                for row in rows:
                    if row['Account Number'] == newId:
                        if 'Password Hash' in row:
                            row['Password Hash'] = passHash
                            
                with open('Tam-Bank/userinfo/accounts.csv', 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
            
            if originalId in self.accounts:
                account = self.accounts.pop(originalId)
                account.accountNumber = newId
                account.fName = fname
                account.lName = lname
                account.mobileNo = mobile
                account.email = email
                account.status = status
                self.accounts[newId] = account
            
            self.getAllAccounts()
            
            return True
            
        except Exception as e:
            print(f"Error updating account: {e}")
            return False

    def adminSetPassword(self, accountId, newPass):
        """Set a password for an account with admin privileges (no validation)"""
        passHash = hashlib.sha256(newPass.encode()).hexdigest()
        
        account = self.getAccount(accountId)
        if account:
            account.passHash = passHash
        
        passwordData = []
        updated = False
        
        try:
            with open('Tam-Bank/userinfo/password.csv', 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                
                for row in reader:
                    if row['accountid'] == accountId:
                        row['password'] = passHash
                        updated = True
                    
                    passwordData.append(row)
            
            if not updated:
                passwordData.append({
                    'accountid': accountId,
                    'password': passHash
                })
            
            with open('Tam-Bank/userinfo/password.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(passwordData)
            
            return True
            
        except Exception:
            return False

    def adminDeleteAccount(self, accountId):
        """Delete an account permanently (admin function)"""
        import csv
        import os
        
        try:
            accountIdStr = str(accountId).strip()
            print(f"Attempting to delete account: {accountIdStr}")
            
            accountsFilePath = 'Tam-Bank/userinfo/accounts.csv'
            if not os.path.exists(accountsFilePath):
                print(f"Error: Accounts file not found at {accountsFilePath}")
                return False
                
            accountsData = []
            accountFound = False
            
            with open(accountsFilePath, 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                
                for row in reader:
                    rowId = str(row['Account Number']).strip()
                    
                    if rowId != accountIdStr:
                        accountsData.append(row)
                    else:
                        accountFound = True
            
            if not accountFound:
                return False
            
            try:
                with open(accountsFilePath, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(accountsData)
            except PermissionError:
                return False
            except Exception as writeErr:
                return False
            
            
            try:
                transFile = 'Tam-Bank/userinfo/transactions.csv'
                if os.path.exists(transFile):
                    transData = []
                    
                    with open(transFile, 'r') as file:
                        reader = csv.DictReader(file)
                        transFieldnames = reader.fieldnames
                        
                        for row in reader:
                            if str(row['from_account']).strip() == accountIdStr:
                                row['from_account'] = "[DELETED]"
                            if str(row['to_account']).strip() == accountIdStr:
                                row['to_account'] = "[DELETED]"
                            transData.append(row)
                    
                    with open(transFile, 'w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=transFieldnames)
                        writer.writeheader()
                        writer.writerows(transData)
                        print("Successfully updated transactions file")
            except Exception as transErr:
                print(f"Note: Error updating transactions: {transErr}")
            
            if accountIdStr in self.accounts:
                del self.accounts[accountIdStr]
            return True
                
        except Exception as e:
            return False

    def isAdmin(self, accountId):
        """Check if an account is the admin account"""
        try:
            return accountId.lower() == 'admin'
        except:
            return False

    def getSystemStats(self):
        """Get system statistics for admin dashboard"""
        stats = {
            'total_accounts': 0,
            'active_accounts': 0,
            'total_balance': 0.0,
            'recent_transactions': 0
        }
        
        accounts = self.getAllAccounts()
        stats['total_accounts'] = len(accounts)
        
        for account in accounts:
            if account.status.lower() == 'active':
                stats['active_accounts'] += 1
            stats['total_balance'] += account.balance
        
        try:
            with open('Tam-Bank/userinfo/transactions.csv', 'r') as file:
                reader = csv.DictReader(file)
                weekAgo = datetime.now() - timedelta(days=7)
                
                for row in reader:
                    try:
                        transDate = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                        if transDate >= weekAgo:
                            stats['recent_transactions'] += 1
                    except:
                        pass
        except Exception:
            pass
        
        return stats
    
    def findAccount(self, accountId):
        """Improved account lookup that handles different formats and whitespace"""
        if accountId in self.accounts:
            return self.accounts[accountId]
            
        normId = str(accountId).strip()
        for accId, account in self.accounts.items():
            if str(accId).strip() == normId:
                return account
        
        try:
            with open('Tam-Bank/userinfo/accounts.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rowId = str(row['Account Number']).strip()
                    if rowId == normId:
                        account = Account(
                            rowId,
                            row['First Name'],
                            row['Last Name'],
                            float(row['Balance']),
                            row['Mobile Number'],
                            row['Email'],
                            row.get('Password Hash', None)
                        )
                        
                        try:
                            account.dateOpened = datetime.strptime(row['Date Opened'], '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            account.dateOpened = datetime.now()
                            
                        account.status = row['Status'] if 'Status' in row else "Active"
                        
                        self.accounts[rowId] = account
                        
                        return account
        except Exception:
            pass
            
        return None
    
    def updateAdminPassword(self, oldPassword, newPassword):
        """Update the admin password with debugging and thorough file updates"""
        import csv
        import hashlib
        import os

        success, message = self.authPass("admin", oldPassword)
        if not success:
            return False
        
        admin = self.getAccount("admin")
        if not admin:
            return False
        
        newHash = hashlib.sha256(newPassword.encode()).hexdigest()
        print(f"Generated new hash: {newHash[:10]}...")
        
        admin.passHash = newHash
        
        csv_success = self._updatePasswordInCSV('Tam-Bank/userinfo/accounts.csv', 'Account Number', 'admin', 'Password Hash', newHash)
        
        pwdFile = 'Tam-Bank/userinfo/password.csv'
        pwdSuccess = True
        if os.path.exists(pwdFile):
            pwdSuccess = self._updatePasswordInCSV(pwdFile, 'accountid', 'admin', 'password', newHash)
        
        self.getAllAccounts()
        
        return csv_success and pwdSuccess

    def _updatePasswordInCSV(self, filePAth, idField, idValue, pwdField, newHash):
        """Update a password in a CSV file with proper error handling"""
        import csv
        import os
        
        print(f"Updating password in {filePAth}...")
        
        if not os.path.exists(filePAth):
            print(f"File not found: {filePAth}")
            return False
        
        try:
            rows = []
            fieldnames = None
            found = False
            
            with open(filePAth, 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                
                for row in reader:
                    if row.get(idField, '').lower() == idValue.lower():
                        row[pwdField] = newHash
                        found = True
                    rows.append(row)
            
            if found:
                with open(filePAth, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                print(f"Successfully updated {filePAth}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error updating {filePAth}: {str(e)}")

    def _validateAccountStatus(self, account, operation="transaction"):
        """ Validate that an account is in the appropriate status for transactions """
        if not account:
            return False, "Account not found"
            
        status = account.status.lower()
        
        if status == "active":
            return True, ""
        elif status == "closed":
            return False, f"Cannot perform {operation}: Account is closed"
        elif status == "suspended":
            return False, f"Cannot perform {operation}: Account is suspended"
        else:  # "inactive" or any other status
            return False, f"Cannot perform {operation}: Account is {account.status}"
            