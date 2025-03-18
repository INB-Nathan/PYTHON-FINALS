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
            self.logo = PhotoImage(file = 'Tam-Bank/GUI/logo.png')
            self.titleLogo = PhotoImage(file = 'Tam-Bank/GUI/TamBank.png')
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

        success,message = self.bank.authPass(txtID.get(), txtPass.get())
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
        registerScreen.grab_set() # Ensures login window cannot be accessed while this is active

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
        
        # password checkingi if d same
        if fields ['Password'].get() != fields['Confirm Password'].get():
            messagebox.showerror('Error', 'Passwords do not match.')
            return
        
        password = fields['Password'].get()
        has_digit = any(char.isdigit() for char in password)
        has_letter = any(char.isalpha() for char in password)
        has_special = any(not char.isalnum() for char in password)

        if len(password) < 6 or not has_digit or not has_letter or not has_special:
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
            messagebox.showerror('Error', f'Failed to create account: str(e)')

    def _updateAccount(self, fields, window):
        try:
            # Validate input fields
            for field, entry in fields.items():
                if not entry.get().strip():
                    messagebox.showerror('Error', f'{field} field cannot be empty.')
                    return

            # Extract input values
            fName = fields['First Name'].get()
            lName = fields['Last Name'].get()
            mobileNo = fields['Phone Number'].get()
            email = fields['Email'].get()

            # Ensure accountNumber is passed correctly
            accountNumber = self.activeAccount.accountNumber

            # Call update function from the bank system
            success, message = self.bank.updateAccount(fName, lName, mobileNo, email, accountNumber)

            if success:
                messagebox.showinfo('Success', 'Account successfully updated!')
                window.destroy()
            else:
                messagebox.showerror('Error', message)

        except Exception as e:
            messagebox.showerror('Error', f'Failed to update account: {str(e)}')
            print(f"Exception occurred: {e}")  # Debugging

    def showUserScreen(self):
        """ Display the user dashboard with button-based navigation """
        self.mainWindow = Tk()
        self.mainWindow.title(f'Tambank - Welcome {self.activeAccount.fName}!')
        self.mainWindow.geometry('1024x768')
        self.mainWindow.resizable(True, True)

        # try except block for images
        try:
            self.logo = PhotoImage(file = 'Tam-Bank/GUI/logo.png')
        except:
            self.logo = None

        # Create main container frames
        headerFrame = Frame(self.mainWindow, bg='#f0f0f0')
        headerFrame.pack(fill=X, padx=10, pady=5)
        
        contentFrame = Frame(self.mainWindow)
        contentFrame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # Create the frames for different sections
        accountFrame = Frame(contentFrame)
        depositFrame = Frame(contentFrame)
        withdrawFrame = Frame(contentFrame)
        transferFrame = Frame(contentFrame)
        accountHistoryFrame = Frame(contentFrame)
        changeUpdateFrame = Frame(contentFrame)
        changePassFrame = Frame(contentFrame)
        closeFrame = Frame(contentFrame)
        
        # Store all frames in a dictionary for easy access
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
        activeColor = '#4CAF50'
        normalColor = '#f0f0f0'
        
        btnAccount = Button(headerFrame, text='Account Details', font=btnFont, 
                        command=lambda: self._showFrame('account'),
                        relief=RAISED, bd=2, padx=5)
        btnDeposit = Button(headerFrame, text='Deposit', font=btnFont,
                        command=lambda: self._showFrame('deposit'),
                        relief=RAISED, bd=2, padx=5)
        btnWithdraw = Button(headerFrame, text='Withdraw', font=btnFont,
                        command=lambda: self._showFrame('withdraw'),
                        relief=RAISED, bd=2, padx=5)
        btnTransfer = Button(headerFrame, text='Transfer', font=btnFont,
                        command=lambda: self._showFrame('transfer'),
                        relief=RAISED, bd=2, padx=5)
        btnHistory = Button(headerFrame, text='Transaction History', font=btnFont,
                        command=lambda: self._showFrame('history'),
                        relief=RAISED, bd=2, padx=5)
        btnUpdate = Button(headerFrame, text='Update Details', font=btnFont,
                        command=lambda: self._showFrame('update'),
                        relief=RAISED, bd=2, padx=5)
        btnPassword = Button(headerFrame, text='Change Password', font=btnFont,
                        command=lambda: self._showFrame('password'),
                        relief=RAISED, bd=2, padx=5)
        btnClose = Button(headerFrame, text='Close Account', font=btnFont,
                        command=lambda: self._showFrame('close'),
                        relief=RAISED, bd=2, padx=5)

        btnAccount.pack(side=LEFT, padx=5, pady=5)
        btnDeposit.pack(side=LEFT, padx=5, pady=5)
        btnWithdraw.pack(side=LEFT, padx=5, pady=5)
        btnTransfer.pack(side=LEFT, padx=5, pady=5)
        btnHistory.pack(side=LEFT, padx=5, pady=5)
        btnUpdate.pack(side=LEFT, padx=5, pady=5)
        btnPassword.pack(side=LEFT, padx=5, pady=5)
        btnClose.pack(side=LEFT, padx=5, pady=5)
        
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
        """ Show the selected frame and hide others """
        for frame in self.frames.values():
            frame.pack_forget()
        
        self.frames[frame_name].pack(fill=BOTH, expand=True)


    def _setupAccountDetails(self, frame):
        """ Display account details """
        header = Label(frame, text='Account Details', font=('Helvetica', 24, 'bold'))
        header.pack(pady=20)

        detailsFrame = Frame(frame)
        detailsFrame.pack(pady=20, fill=X, padx = 50)

        account = self.activeAccount

        fields = [
            ('Account Number', account.accountNumber),
            ('First Name', account.fName),
            ('Last Name', account.lName),
            ('Phone Number', account.mobileNo),
            ('Email', account.email),
            ('Balance', f'${account.balance:.2f}'),
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
        
        refresh_btn = Button(frame, text="Refresh", font=('Helvetica', 12),
                        command=lambda: self._refreshAccountDetails(frame))
        refresh_btn.pack(pady=20)

    
    def _setupDeposit(self, frame):
        pass

    def _setupWithdraw(self, frame):
        pass

    def _setupTransfer(self, frame):
        pass

    def _setupAccountHistory(self, frame):
        pass

    def _setupUpdateDetails(self, frame):
        """ Display update account """
        header = Label(frame, text='Update Account', font=('Helvetica', 24, 'bold'))
        header.pack(pady=20)

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
            entry.insert(0, value)  # Pre-fill existing data
            
            fields[labelText] = entry
        
        btnFrame = Frame(updateFrame)
        btnFrame.pack(pady=20)
        
        btnUpdate = Button(btnFrame, text='Update', font=('Helvetica', 12), 
                           command=lambda: self._updateAccount(fields, updateFrame))
        
        btnUpdate.pack(side=LEFT, padx=10)

    def _setupChangePassword(self, frame):
        pass

    def _setupCloseAccount(self, frame):
        pass

    def _logout(self):
        self.activeAccount = None
        self.mainWindow.destroy()
        self.loginScreen()


