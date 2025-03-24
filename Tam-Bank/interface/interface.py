from tkinter import *
from tkinter import messagebox  # for pop-up message windows
from tkinter import ttk

class GUIinterface:
    """ GUI interface """

    def __init__(self, bankService):
        """ Initialize the GUI interface with a reference to the TAMBANK object """
        self.bank = bankService
        self.activeAccount = None
        self.mainWindow = None
        self.frames = {}
        self.navigator = {}

    def start(self):
        """ Start the GUI with the login screen """    
        self.loginScreen()

    def loginScreen(self):
        """First screen to authenticate users"""
        # Styling Variables
        defaultFont = ('Helvetica', 20, 'bold')
        btnFont = ('Helvetica', 12, 'bold')

        # if existing mainWindow is present, destroy
        if self.mainWindow:
            self.mainWindow.destroy()
        
        # Create the main window with the following properties
        self.mainWindow = Tk()
        self.mainWindow.title('TamBank')
        self.mainWindow.geometry("800x600+400+100")
        self.mainWindow.resizable(False,False)

        # load images using try except block so that if there is no images found just set the title_logo to none to not confuse users
        try:
            self.logo = PhotoImage(file = 'Tam-Bank/graphics/logo.png')
            self.titleLogo = PhotoImage(file = 'Tam-Bank/graphics/TamBank.png')
            self.mainWindow.iconphoto(True, self.logo)
        except:
            self.titleLogo = None
        
        # Create widgets
        if self.titleLogo:
            lblTitle = Label(self.mainWindow, image = self.titleLogo)
            lblTitle.pack(pady = 100)
        else:
            lblTitle = Label(self.mainWindow, text = 'TamBank', font = ('Arial', 30, 'bold'))
            lblTitle.pack(pady = 100)
        
        lblAccountID = Label(self.mainWindow, text = 'Account ID:', font = defaultFont)
        lblPassword = Label(self.mainWindow, text = 'Password:', font = defaultFont)
        txtID = Entry(self.mainWindow, font = defaultFont)
        txtPass = Entry(self.mainWindow, font = defaultFont, show= '*')
        btnLogin = Button(self.mainWindow, text = 'Login', font = btnFont, padx = 15, command = lambda: self._authenticate(txtID, txtPass))
        btnRegister = Button(self.mainWindow, text = 'Register', font = btnFont, padx = 15, command = lambda: self._showRegisterScreen())

        # place the widgets
        lblAccountID.place(x = 160, y = 300)
        lblPassword.place(x = 175, y = 350)
        txtID.place(x = 340, y = 300)
        txtPass.place(x = 340, y = 350)
        btnLogin.place(x = 450, y = 400)
        btnRegister.place(x = 555, y = 400)

        self.mainWindow.mainloop()

    
    def _authenticate(self, txtID, txtPass):
        """Validates login and opens corresponding screen if credentials match."""
        if not txtID.get() or not txtPass.get():
            messagebox.showerror('Login Failed', 'Please enter your Account Number and Password')
            return
        
        accountId = txtID.get()
        password = txtPass.get()

        if accountId == "admin":
            success, message = self.bank.authPass(accountId, password)
            if success:
                self.mainWindow.destroy()
                self._adminInterface()
            else:
                messagebox.showerror('Login Failed', message)
                txtPass.delete(0, END)
            return
        
        account = self.bank.getAccount(accountId)
        if not account:
            messagebox.showerror('Login Failed', 'Account not found.')
            return

        if account.status.lower() == 'closed':
            messagebox.showerror('Login Failed', 'Account is closed.')
            return
        
        if account.status.lower() == 'suspended':
            messagebox.showerror('Login Failed', 'Account is suspended.')
            return
        
        success, message = self.bank.authPass(txtID.get(), txtPass.get())
        if success:
            self.activeAccount = self.bank.getAccount(txtID.get())
            self.mainWindow.destroy()
            self.showUserScreen()
        else:
            messagebox.showerror('Login Failed', message)
            txtPass.delete(0, END)


    def _showRegisterScreen(self):
        """ Window for creating new accounts """
        # styling
        lblFont = ('Arial', 18, 'bold')
        txtFont = ('Arial', 18)
        btnFont = ('Arial', 16)

        registerScreen = Toplevel(self.mainWindow)
        registerScreen.title('Create Account')
        registerScreen.geometry('800x600')
        registerScreen.resizable(False, False)
        registerScreen.grab_set()

        # header
        lblHeader = Label(registerScreen, text='Enter user details', font=('Arial', 24, 'bold'))
        lblHeader.grid(row=0, column=0, columnspan=2, pady=20)

        fields = {}
        row = 1

        for field in ['First Name', 'Last Name', 'Phone Number', 'Email', 'Balance', 'Password', 'Confirm Password']:
            lbl = Label(registerScreen, text=f'{field}:', font=lblFont)
            lbl.grid(row=row, column=0, sticky='w', padx=20, pady=10)
            if 'Password' in field:
                txt = Entry(registerScreen, font=txtFont, show='*')
            else:
                txt = Entry(registerScreen, font=txtFont)
            txt.grid(row=row, column=1, padx=20, pady=5)
            fields[field] = txt
            row += 1

        btnFrame = Frame(registerScreen)
        btnFrame.grid(row=row, column=0, columnspan=2, pady=20)
        btnCreate = Button(btnFrame, text='Submit', font=btnFont, command=lambda: self._registerAccount(fields, registerScreen))
        btnCancel = Button(btnFrame, text='Cancel', font=btnFont, command=registerScreen.destroy)

        btnCreate.pack(side=LEFT, padx=20)
        btnCancel.pack(side=RIGHT, padx=20)

        registerScreen.mainloop()
    
    def _registerAccount(self, fields, window):
        """ register a new account with the bank service """
        # create basic validation first
        for field, entry in fields.items():
            if not entry.get().strip() and field != 'Balance':
                messagebox.showerror('Error', f'{field} field cannot be empty.')
                return
            
        # name validation
        fName = fields['First Name'].get()
        lName = fields['Last Name'].get()
        if not fName.isalpha() or not lName.isalpha():
            messagebox.showerror('Error', 'First and Last name must only contain letters.')
            return
        
        # phone number validation
        phone = fields['Phone Number'].get()
        if not (phone.isdigit() and phone.startswith('09') and len(phone) == 11):
            messagebox.showerror('Error', 'Invalid phone number. It should start with 09 and have 11 digits.')
            return
        
        # email validation
        email = fields['Email'].get()
        if '@' not in email or '.' not in email:
            messagebox.showerror('Error', 'Invalid email format.')
            return
        
        # password checkingi if d same
        if fields ['Password'].get() != fields['Confirm Password'].get():
            messagebox.showerror('Error', 'Passwords do not match.')
            return
            
        
        password = fields['Password'].get()
        hasDigit = any(char.isdigit() for char in password)
        hasLetter = any(char.isalpha() for char in password)
        hasSpecial = any(not char.isalnum() for char in password)

        if len(password) < 6 or not hasDigit or not hasLetter or not hasSpecial:
            messagebox.showerror('Error', 'Password must be at least 6 characters long and contain at least one letter, number, and special character.')
            return


        # initial balance checker
        try:
            initialBal = float(fields['Balance'].get() if fields['Balance'].get() else 0)
            if initialBal < 0:
                messagebox.showerror('Error', 'Initial balance cannot be negative.')
                return
        except ValueError:
            messagebox.showerror('Error', 'Initial balance must be a valid number.')
            return

        # try to create the account
        try:
            account = self.bank.createAccount(
                fields['First Name'].get(),
                fields['Last Name'].get(),
                initialBal,
                fields['Phone Number'].get(),
                fields['Email'].get(),
                fields['Password'].get()
            )
            
            messagebox.showinfo('Success', f'Account successfully created!\nYour account number is: {account.accountNumber}\n' f'Login to continue.')
            window.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to create account: {str(e)}')

    def _updateAccount(self, fields, window):
        try:
            for field, entry in fields.items():
                if not entry.get().strip():
                    messagebox.showerror('Error', f'{field} field cannot be empty.')
                    return

            fName = fields['First Name'].get()
            lName = fields['Last Name'].get()
            mobileNo = fields['Phone Number'].get()
            email = fields['Email'].get()

            if not fName.isalpha() or not lName.isalpha():
                messagebox.showerror('Error', 'First and Last name must only contain letters.')
                return
            
            # phone number validation
            if not (mobileNo.isdigit() and mobileNo.startswith('09') and len(mobileNo) == 11):
                messagebox.showerror('Error', 'Invalid phone number. It should start with 09 and have 11 digits.')
                return

            # email validation
            if '@' not in email or '.' not in email:
                messagebox.showerror('Error', 'Invalid email format.')
                return

            accountNumber = self.activeAccount.accountNumber

            success, message = self.bank.updateAccount(fName, lName, mobileNo, email, accountNumber)

            if success:
                messagebox.showinfo('Success', 'Account successfully updated!')
            else:
                messagebox.showerror('Error', message)

        except Exception as e:
            messagebox.showerror('Error', f'Failed to update account: {str(e)}')
            print(f"Exception occurred: {e}")
    
    def _depositFunds(self, txtAmount):
        """ Handle deposit action """
        try:
            amount = float(txtAmount.get())
            if amount <= 0:
                messagebox.showerror('Error', 'Deposit amount must be greater than zero.')
                return
    
            success, message = self.bank.deposit(self.activeAccount.accountNumber, amount)
            if success:
                messagebox.showinfo('Success', message)
            else:
                messagebox.showerror('Error', message)
        except ValueError:
            messagebox.showerror('Error', 'Invalid amount entered.')
    
    def _withdrawFunds(self, txtAmount):
        """ Handle withdraw action """
        try:
            amount = float(txtAmount.get())
            if amount <= 0:
                messagebox.showerror('Error', 'Withdrawal amount must be greater than zero.')
                return
    
            success, message = self.bank.withdraw(self.activeAccount.accountNumber, amount)
            if success:
                messagebox.showinfo('Success', message)
            else:
                messagebox.showerror('Error', message)
        except ValueError:
            messagebox.showerror('Error', 'Invalid amount entered.')

    def _changePassword(self, txtOldPass, txtNewPass, txtConfirmPass):
        """ Handle change password action """
        oldPass = txtOldPass.get()
        newPass = txtNewPass.get()
        confirmPass = txtConfirmPass.get()
    
        if not oldPass or not newPass or not confirmPass:
            messagebox.showerror('Error', 'All fields must be filled.')
            return
    
        if newPass != confirmPass:
            messagebox.showerror('Error', 'New Password and Confirm Password do not match.')
            return
            
        hasDigit = any(char.isdigit() for char in newPass)
        hasLetter = any(char.isalpha() for char in newPass)
        hasSpecial = any(not char.isalnum() for char in newPass)

        if len(newPass) < 8 or not hasDigit or not hasLetter or not hasSpecial:
            messagebox.showerror('Error', 'Password must be at least 8 characters long and contain at least one letter, number, and special character.')
            return

        try:
            success = self.bank.changePass(self.activeAccount.accountNumber, oldPass, newPass)
            if success:
                messagebox.showinfo('Success', "Password successfully changed.")
            else:
                messagebox.showerror('Error', "Failed to change password.")
        except Exception as e:
            messagebox.showerror('Error', f'Failed to change password: {str(e)}')

    def showUserScreen(self):
        """ Display the user dashboard with button-based navigation """
        self.mainWindow = Tk()
        self.mainWindow.title(f'Tambank - Welcome {self.activeAccount.fName}!')
        self.mainWindow.geometry('1024x768')
        self.mainWindow.resizable(True, True)

        # try except block for images
        try:
            self.logo = PhotoImage(file = 'Tam-Bank/graphics/logo.png')
        except:
            self.logo = None

        headerFrame = Frame(self.mainWindow, bg='#f0f0f0')
        headerFrame.pack(fill=X)
        
        contentFrame = Frame(self.mainWindow)
        contentFrame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        accountFrame = Frame(contentFrame)
        depositFrame = Frame(contentFrame)
        withdrawFrame = Frame(contentFrame)
        transferFrame = Frame(contentFrame)
        accountHistoryFrame = Frame(contentFrame)
        changeUpdateFrame = Frame(contentFrame)
        changePassFrame = Frame(contentFrame)
        closeFrame = Frame(contentFrame)
        
        self.frames = {
            'account': accountFrame,
            'deposit': depositFrame,
            'withdraw': withdrawFrame,
            'transfer': transferFrame,
            'history': accountHistoryFrame,
            'password': changePassFrame,
            'close': closeFrame,
            'update': changeUpdateFrame
        }
        
        # Create navigation buttons
        btnFont = ('Helvetica', 11, 'bold')
        normalColor = '#f0f0f0'

        btnAccount = Button(headerFrame, text='Account Details', font=btnFont, 
                command=lambda: self._showFrame('account'),
                relief=RAISED, bd=2, padx=5,
                bg=normalColor)
        btnDeposit = Button(headerFrame, text='Deposit', font=btnFont,
                        command=lambda: self._showFrame('deposit'),
                        relief=RAISED, bd=2, padx=5,
                        bg=normalColor)
        btnWithdraw = Button(headerFrame, text='Withdraw', font=btnFont,
                        command=lambda: self._showFrame('withdraw'),
                        relief=RAISED, bd=2, padx=5,
                        bg=normalColor)
        btnTransfer = Button(headerFrame, text='Transfer', font=btnFont,
                        command=lambda: self._showFrame('transfer'),
                        relief=RAISED, bd=2, padx=5,
                        bg=normalColor)
        btnHistory = Button(headerFrame, text='Transaction History', font=btnFont,
                        command=lambda: self._showFrame('history'),
                        relief=RAISED, bd=2, padx=5,
                        bg=normalColor)
        btnUpdate = Button(headerFrame, text='Update Details', font=btnFont,
                        command=lambda: self._showFrame('update'),
                        relief=RAISED, bd=2, padx=5,
                        bg=normalColor)
        btnPassword = Button(headerFrame, text='Change Password', font=btnFont,
                        command=lambda: self._showFrame('password'),
                        relief=RAISED, bd=2, padx=5,
                        bg=normalColor)
        btnClose = Button(headerFrame, text='Close Account', font=btnFont,
                        command=lambda: self._showFrame('close'),
                        relief=RAISED, bd=2, padx=5,
                        bg=normalColor)
        
        self.navigator = {
            'account': btnAccount,
            'deposit': btnDeposit,
            'withdraw': btnWithdraw,
            'transfer': btnTransfer,
            'history': btnHistory,
            'password': btnPassword,
            'close': btnClose,
            'update': btnUpdate
        }

        btnAccount.pack(side=LEFT, fill='both', expand=True)
        btnDeposit.pack(side=LEFT, fill='both', expand=True)
        btnWithdraw.pack(side=LEFT, fill='both', expand=True)
        btnTransfer.pack(side=LEFT, fill='both', expand=True)
        btnHistory.pack(side=LEFT, fill='both', expand=True)
        btnUpdate.pack(side=LEFT, fill='both', expand=True)
        btnPassword.pack(side=LEFT, fill='both', expand=True)
        btnClose.pack(side=LEFT, fill='both', expand=True)
        
        self._setupAccountDetails(accountFrame)
        self._setupDeposit(depositFrame)
        self._setupWithdraw(withdrawFrame)
        self._setupTransfer(transferFrame)
        self._setupAccountHistory(accountHistoryFrame)
        self._setupUpdateDetails(changeUpdateFrame)
        self._setupChangePassword(changePassFrame)
        self._setupCloseAccount(closeFrame)
        
        logoutbtn = Button(self.mainWindow, text = 'Logout', font = ('Helvetica', 12, 'bold'), command = self._logout)
        logoutbtn.pack(pady=10)
        
        self._showFrame('account')
        
        self.mainWindow.mainloop()

    def _showFrame(self, frame_name):
        """ Show the selected frame, hide others, then changes the button fg to active """
        activeColor = '#4CAF50'
        normalColor = '#f0f0f0'
        
        for frame in self.frames.values():
            frame.pack_forget()
        
        self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)

        for widget in self.frames[frame_name].winfo_children():
            widget.destroy()

        if frame_name == 'account':
            self._setupAccountDetails(self.frames[frame_name])
        elif frame_name == 'deposit':
            self._setupDeposit(self.frames[frame_name])
        elif frame_name == 'withdraw':
            self._setupWithdraw(self.frames[frame_name])
        elif frame_name == 'transfer':
            self._setupTransfer(self.frames[frame_name])
        elif frame_name == 'history':
            self._setupAccountHistory(self.frames[frame_name])
        elif frame_name == 'update':
            self._setupUpdateDetails(self.frames[frame_name])
        elif frame_name == 'password':
            self._setupChangePassword(self.frames[frame_name])
        elif frame_name == 'close':
            self._setupCloseAccount(self.frames[frame_name])
        
        self.frames[frame_name].pack(fill=BOTH, expand=True)
        
        for name, btn in self.navigator.items():
            if name == frame_name:
                btn.config(bg=activeColor, fg='white')
            else:
                btn.config(bg=normalColor, fg='black')
            


    def _setupAccountDetails(self, frame):
        """ Display account details """
        header = Label(frame, text='Account Details', font=('Helvetica', 24, 'bold'))
        header.pack(pady=20)

        self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)
        
        detailsFrame = Frame(frame)
        detailsFrame.pack(pady=20, fill=X, padx = 50)

        account = self.activeAccount

        fields = [
            ('Account Number', account.accountNumber),
            ('First Name', account.fName),
            ('Last Name', account.lName),
            ('Phone Number', account.mobileNo),
            ('Email', account.email),
            ('Balance', f'PHP {account.balance:.2f}'),
            ('Date Opened', account.dateOpened.strftime('%Y-%m-%d')),
            ('Status', account.status)
        ]

        for i, (labelText, value) in enumerate(fields):
            rowFrame = Frame(detailsFrame)
            rowFrame.pack(fill=X, pady=5)
            
            label = Label(rowFrame, text=f"{labelText}:", font=('Helvetica', 14, 'bold'), width=15, anchor='w')
            label.pack(side=LEFT)
            
            value_label = Label(rowFrame, text=str(value), font=('Helvetica', 14))
            value_label.pack(side=LEFT, padx=10)

    def _setupDeposit(self, frame):
        """ interface for depositing"""
        header = Label(frame, text='Deposit Money', font=('Helvetica', 24, 'bold'))
        header.pack(pady=20)

        self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)


        depoFrame = Frame(frame)
        depoFrame.pack(pady=20, padx=50)

        balFrame = Frame(depoFrame)
        balFrame.pack(fill = X, pady=10)
        balLabel = Label(balFrame, text = 'Current Balance:', font = ('Helvetica', 16, 'bold'))
        balLabel.pack(side = LEFT)
        balVal = Label(balFrame, text = f"PHP {self.activeAccount.balance:.2f}", font = ('Helvetica', 16))
        balVal.pack(side = LEFT, padx = 10)

        amountFrame = Frame(depoFrame)
        amountFrame.pack(fill = X, pady=20)
        amountLabel = Label(amountFrame, text = 'Amount:', font = ('Helvetica', 16, 'bold'))
        amountLabel.pack(side = LEFT)
        amountEntry = Entry(amountFrame, font = ('Helvetica', 16), width = 20)
        amountEntry.pack(side = LEFT, padx = 10)

        depositBtn = Button(depoFrame, text="Deposit", font=('Helvetica', 14, 'bold'), bg='#4CAF50', fg='white', padx=20, pady=5, command=lambda: self._processDeposit(amountEntry, balVal))
        depositBtn.pack(side = RIGHT)

    def _processDeposit(self, amount_entry, balanceLabel):
        """ deposit money into account """
        try:
            amount_string = amount_entry.get()
            amount_value = float(amount_string)

            if amount_value <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0.")
                return
                
            success, message = self.bank.deposit(self.activeAccount.accountNumber, amount_value)

            if success:
                messagebox.showinfo("Success", message)
                self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)
                balanceLabel.config(text=f"PHP {self.activeAccount.balance:.2f}")
                amount_entry.delete(0, END)  
            else:
                messagebox.showerror("Error", message)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount.")
                
    def _processWithdraw(self, amount_entry, balanceLabel):
        """ withdraw transaction backend """
        try:
            amount_string = amount_entry.get()
            amount_value = float(amount_string)
            
            if amount_value <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0.")
                return
                
            success, message = self.bank.withdraw(self.activeAccount.accountNumber, amount_value)

            if success:
                messagebox.showinfo("Success", message)
                self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)
                balanceLabel.config(text=f"PHP {self.activeAccount.balance:.2f}")
                amount_entry.delete(0, END)
            else:
                messagebox.showerror("Error", message)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount.")

    def _setupWithdraw(self, frame):
        """ withdraw money from account """
        header = Label(frame, text='Withdraw Money', font=('Helvetica', 24, 'bold'))
        header.pack(pady=20)

        self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)

        withdrawFrame = Frame(frame)
        withdrawFrame.pack(pady=20, padx=50)
        balFrame = Frame(withdrawFrame)
        balFrame.pack(fill = X, pady=10)

        balLabel = Label(balFrame, text = 'Current Balance:', font = ('Helvetica', 16, 'bold'))
        balLabel.pack(side = LEFT)
        balVal = Label(balFrame, text = f"PHP {self.activeAccount.balance:.2f}", font = ('Helvetica', 16))
        balVal.pack(side = LEFT, padx = 10)

        amountFrame = Frame(withdrawFrame)
        amountFrame.pack(fill = X, pady=20)
        amountLabel = Label(amountFrame, text = 'Amount:', font = ('Helvetica', 16, 'bold'))
        amountLabel.pack(side = LEFT)
        amountEntry = Entry(amountFrame, font = ('Helvetica', 16), width = 20)
        amountEntry.pack(side = LEFT, padx = 10)

        withdrawBtn = Button(withdrawFrame, text="Withdraw", font=('Helvetica', 14, 'bold'), bg='#4CAF50', fg='white', padx=20, pady=5, command=lambda: self._processWithdraw(amountEntry, balVal))
        withdrawBtn.pack(side = RIGHT)

    def _processTransfer(self, toAccEntry, amountEntry, descEntry, balVal):
        """ transfer money between accounts """
    
        # first check the account
        try:
            toAcc_number = toAccEntry.get().strip()
            
            if not toAcc_number:
                messagebox.showerror("Error", "Account not found.")
                return
            
            recipAcc = self.bank.getAccount(toAcc_number)
            if not recipAcc:
                messagebox.showerror("Error", "Recipient account not found.")
                return
            
            if toAcc_number == self.activeAccount.accountNumber:
                messagebox.showerror("Error", "Cannot transfer to own account.")
                return
            
            amount_value = float(amountEntry.get())
            
            if amount_value <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0.")
                return
            
            if amount_value > self.activeAccount.balance:
                messagebox.showerror("Error", "Insufficient funds.")
                return
            
            description = descEntry.get().strip()
            if not description:
                description = f'Transfer to {toAcc_number}'
            
            confirm = messagebox.askyesno("Confirm Transfer", 
                                        f"Transfer PHP {amount_value:.2f} to account {toAcc_number}?\nDescription: {description}")
            if not confirm:
                return
            
            success, message = self.bank.transaction(
                self.activeAccount.accountNumber, toAcc_number, amount_value, description
            )

            if success:
                messagebox.showinfo("Success", message)
                self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)
                balVal.config(text=f"PHP {self.activeAccount.balance:.2f}")
                toAccEntry.delete(0, END)
                amountEntry.delete(0, END)
                descEntry.delete(0, END)
            else:
                messagebox.showerror("Error", message)

        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount.")

    def _setupTransfer(self, frame):
        """Create interface for transferring funds between accounts"""
        header = Label(frame, text="Transfer Funds", font=('Helvetica', 24, 'bold'))
        header.pack(pady=20)

        self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)
        
        transferFrame = Frame(frame)
        transferFrame.pack(pady=20, padx=50)

        balFrame = Frame(transferFrame)
        balFrame.pack(fill=X, pady=10)
        balLabel = Label(balFrame, text="Your Balance:", font=('Helvetica', 16, 'bold'))
        balLabel.pack(side=LEFT)
        balValue = Label(balFrame, text=f"PHP {self.activeAccount.balance:.2f}", font=('Helvetica', 16))
        balValue.pack(side=LEFT, padx=10)
        
        
        toFrame = Frame(transferFrame)
        toFrame.pack(fill=X, pady=10)
        
        toLabel = Label(toFrame, text="To Account:", font=('Helvetica', 16, 'bold'))
        toLabel.pack(side=LEFT)
        
        toEntry = Entry(toFrame, font=('Helvetica', 16), width=20)
        toEntry.pack(side=RIGHT, padx=10)
        
        amountFrame = Frame(transferFrame)
        amountFrame.pack(fill=X, pady=10)
        
        amountLabel = Label(amountFrame, text="Amount:", font=('Helvetica', 16, 'bold'))
        amountLabel.pack(side=LEFT)
        
        amountEntry = Entry(amountFrame, font=('Helvetica', 16), width=20)
        amountEntry.pack(side=RIGHT, padx=10)
        
        descFrame = Frame(transferFrame)
        descFrame.pack(fill=X, pady=10)
        
        descLabel = Label(descFrame, text="Description:", font=('Helvetica', 16, 'bold'))
        descLabel.pack(side=LEFT)
        
        descEntry = Entry(descFrame, font=('Helvetica', 16), width=20)
        descEntry.pack(side=RIGHT, padx=10)
        
        transfer_btn = Button(transferFrame, text="Transfer", font=('Helvetica', 14, 'bold'), bg='#2196F3', fg='white', padx=20, pady=5, command=lambda: self._processTransfer(toEntry, amountEntry, descEntry, balValue))
        transfer_btn.pack(side = RIGHT)

    def _setupAccountHistory(self, frame):
        """Create transaction history interface"""
        for widget in frame.winfo_children():
            widget.destroy()
            
        self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)

        header = Label(frame, text="Transaction History", font=('Helvetica', 24, 'bold'))
        header.pack(pady=20)
        
        treeFrame = Frame(frame)
        treeFrame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        columns = ('date', 'description', 'amount', 'transacId')
        tree = ttk.Treeview(treeFrame, columns=columns, show='headings')
        
        tree.heading('date', text='Date')
        tree.heading('description', text='Description')
        tree.heading('amount', text='Amount')
        tree.heading('transacId', text='Transaction ID')
        
        tree.column('date', width=150)
        tree.column('description', width=250)
        tree.column('amount', width=150)
        tree.column('transacId', width=150)
        
        y_scrollbar = ttk.Scrollbar(treeFrame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=y_scrollbar.set)
        
        y_scrollbar.pack(side=RIGHT, fill=Y)
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        
        try:
            transactions = self.bank.getAccountTransactions(self.activeAccount.accountNumber)
            
            if not transactions:
                tree.insert('', 'end', values=('', 'No transactions found', '', ''))
            else:
                for transaction in transactions:
                    try:
                        if hasattr(transaction['date'], 'strftime'):
                            date_str = transaction['date'].strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            date_str = str(transaction['date'])
                        
                        if float(transaction['amount']) >= 0:
                            amount_str = f"PHP +{float(transaction['amount']):.2f}"
                            tag = 'positive'
                        else:
                            amount_str = f"PHP {float(transaction['amount']):.2f}"
                            tag = 'negative'
                        
                        transacId = transaction.get('transacId', '')
                        description = transaction.get('description', 'Transaction')
                        
                        item_id = tree.insert('', 'end', values=(date_str, description, 
                                                    amount_str, transacId))
                        
                        if tag == 'positive':
                            tree.tag_configure('positive', foreground='green')
                            tree.item(item_id, tags=('positive',))
                        elif tag == 'negative':
                            tree.tag_configure('negative', foreground='red')
                            tree.item(item_id, tags=('negative',))
                            
                    except (KeyError, ValueError, AttributeError) as e:
                        print(f"Error processing transaction: {e}")
                        continue
        except Exception as e:
            messagebox.showerror("Error", f"Could not load transaction history: {e}")
            tree.insert('', 'end', values=('', f'Error: {str(e)}', '', ''))
        
        refreshBtn = Button(frame, text="Refresh History", font=('Helvetica', 12),
                        command=lambda: self._refreshHistory(frame))
        refreshBtn.pack(pady=10)

    def _refreshHistory(self, frame):
        """Refresh the transaction history"""
        try:
            self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)
            self._setupAccountHistory(frame)
            messagebox.showinfo("Success", "Transaction history refreshed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh history: {str(e)}")

    def _setupUpdateDetails(self, frame):
        """ Display update account """
        header = Label(frame, text='Update Account', font=('Helvetica', 24, 'bold'))
        header.pack(pady=20)

        self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)

        updateFrame = Frame(frame)
        updateFrame.pack(pady=20, fill=X, padx = 50)

        fields = {}
        account = self.activeAccount
        field_data = [
            ('First Name', account.fName),
            ('Last Name', account.lName),
            ('Phone Number', account.mobileNo),
            ('Email', account.email)
        ]

        for labelText, value in field_data:
            rowFrame = Frame(updateFrame)
            rowFrame.pack(fill=X, pady=5)
            
            label = Label(rowFrame, text=f"{labelText}:", font=('Helvetica', 14, 'bold'), width=15, anchor='w')
            label.pack(side=LEFT)
            
            entry = Entry(rowFrame, font=('Helvetica', 14))
            entry.pack(side=LEFT, padx=10, fill=X, expand=True)
            entry.insert(0, value)

            fields[labelText] = entry
        
        btnFrame = Frame(updateFrame)
        btnFrame.pack(pady=20)
        
        btnUpdate = Button(btnFrame, text='Update', font=('Helvetica', 12), 
                           command=lambda: self._updateAccount(fields, updateFrame))
        
        btnUpdate.pack(side=LEFT, padx=10)

    def _setupChangePassword(self, frame):
        """ Setup change password functionality """

        self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)


        header = Label(frame, text='Change Password', font=('Helvetica', 24, 'bold'))
        header.pack(pady=20)
    
        oldPassFrame = Frame(frame)
        oldPassFrame.pack(pady=10)
    
        lblOldPass = Label(oldPassFrame, text='Old Password:', font=('Helvetica', 14, 'bold'))
        lblOldPass.pack(side=LEFT)
    
        txtOldPass = Entry(oldPassFrame, font=('Helvetica', 14), show='*')
        txtOldPass.pack(side=RIGHT, padx=10)
    
        newPassFrame = Frame(frame)
        newPassFrame.pack(pady=10)
    
        lblNewPass = Label(newPassFrame, text='New Password:', font=('Helvetica', 14, 'bold'))
        lblNewPass.pack(side=LEFT)
    
        txtNewPass = Entry(newPassFrame, font=('Helvetica', 14), show='*')
        txtNewPass.pack(side=RIGHT, padx=10)
    
        confirmPassFrame = Frame(frame)
        confirmPassFrame.pack(pady=10)
    
        lblConfirmPass = Label(confirmPassFrame, text='Confirm Password:', font=('Helvetica', 14, 'bold'))
        lblConfirmPass.pack(side=LEFT)
    
        txtConfirmPass = Entry(confirmPassFrame, font=('Helvetica', 14), show='*')
        txtConfirmPass.pack(side=RIGHT, padx=5)
    
        btnChangePass = Button(frame, text='Change Password', font=('Helvetica', 12),
                               command=lambda: self._changePassword(txtOldPass, txtNewPass, txtConfirmPass))
        btnChangePass.pack(pady=10)

    def _setupCloseAccount(self, frame):
        """Create interface for closing an account"""
        for widget in frame.winfo_children():
            widget.destroy()

        self.activeAccount = self.bank.getAccount(self.activeAccount.accountNumber)
            
        header = Label(frame, text="Close Account", font=('Helvetica', 24, 'bold'))
        header.pack(pady=20)
        
        warningFrame = Frame(frame, bg='#ffcccc', padx=20, pady=20)
        warningFrame.pack(fill=X, padx=50, pady=10)
        
        warningLabel = Label(warningFrame, 
                            text="⚠️ WARNING: Account closure is permanent! ⚠️", 
                            font=('Helvetica', 16, 'bold'), 
                            fg='red',
                            bg='#ffcccc')
        warningLabel.pack(pady=5)
        
        warningText = Label(warningFrame, 
                        text="• Your account will be permanently closed\n"
                                "• All data associated with this account will be marked as inactive\n"
                                "• You must withdraw or transfer all funds before closing\n"
                                "• You'll need to create a new account if you want to use TamBank again",
                        font=('Helvetica', 12),
                        justify=LEFT,
                        bg='#ffcccc')
        warningText.pack(pady=5, anchor=W)
        
        balanceFrame = Frame(frame)
        balanceFrame.pack(fill=X, padx=50, pady=10)
        
        balanceLabel = Label(balanceFrame, 
                            text=f"Current Balance: PHP {self.activeAccount.balance:.2f}",
                            font=('Helvetica', 14, 'bold'))
        balanceLabel.pack(anchor=W)
        
        if self.activeAccount.balance > 0:
            balanceWarning = Label(balanceFrame, 
                                text="You must withdraw all funds before closing your account",
                                font=('Helvetica', 12),
                                fg='red')
            balanceWarning.pack(anchor=W)
            
            withdrawBtn = Button(balanceFrame, 
                                text="Go to Withdraw", 
                                command=lambda: self._showFrame('withdraw'),
                                font=('Helvetica', 12))
            withdrawBtn.pack(pady=10)
        
        confirmFrame = Frame(frame)
        confirmFrame.pack(fill=X, padx=50, pady=20)
        
        passwordLabel = Label(confirmFrame, 
                            text="Enter your password to confirm account closure:",
                            font=('Helvetica', 12, 'bold'))
        passwordLabel.pack(anchor=W, pady=5)
        
        passwordEntry = Entry(confirmFrame, show="*", font=('Helvetica', 12), width=30)
        passwordEntry.pack(anchor=W)
        
        confirmVar = IntVar()
        confirmCheck = Checkbutton(confirmFrame, 
                                    text="I understand that closing my account is permanent and cannot be undone",
                                    variable=confirmVar,
                                    font=('Helvetica', 12))
        confirmCheck.pack(anchor=W, pady=10)
        
        btnFrame = Frame(frame)
        btnFrame.pack(pady=20)
        
        cancelBtn = Button(btnFrame, 
                            text="Cancel", 
                            font=('Helvetica', 14),
                            padx=20,
                            command=lambda: self._showFrame('account'))
        cancelBtn.pack(side=LEFT, padx=10)
        
        closeBtn = Button(btnFrame, 
                            text="Close Account", 
                            font=('Helvetica', 14, 'bold'),
                            bg='#f44336',
                            fg='white',
                            padx=20,
                            command=lambda: self._processAccountClosure(passwordEntry
                , confirmVar))
        closeBtn.pack(side=LEFT, padx=10)

    def _processAccountClosure(self, passwordEntry, confirmVar):
        """Process the account closure request"""
        if confirmVar.get() != 1:
            messagebox.showerror("Error", "You must confirm that you understand the consequences of account closure")
            return
            
        password = passwordEntry.get()
        if not password:
            messagebox.showerror("Error", "Please enter your password")
            return
            
        success, _ = self.bank.authPass(self.activeAccount.accountNumber, password)
        if not success:
            messagebox.showerror("Error", "Invalid password")
            return
            
        if self.activeAccount.balance > 0:
            messagebox.showerror("Error", "You must withdraw all funds before closing your account")
            return
            
        success, message = self.bank.closeAccount(self.activeAccount.accountNumber)
        
        if success:
            messagebox.showinfo("Account Closed", message)
            self._logout()
        else:
            messagebox.showerror("Error", f"Failed to close account: {message}")

    def _logout(self):
        self.activeAccount = None
        self.loginScreen()

    def _adminInterface(self):
        """ Starting The Admin Interface """
        from interface.aInterface import AdminGUIinterface
        
        adminGUI = AdminGUIinterface(self.bank)
        adminGUI.start()


