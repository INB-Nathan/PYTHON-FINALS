from tkinter import *
from tkinter import messagebox  # for pop-up message windows

def authenticate(sc, txtID, txtPass):
    """Validates login and opens corresponding screen if credentials match."""
    if txtID.get() == 'admin' and txtPass.get() == 'admin':  # placeholder
        sc.destroy()
        adminScreen()
    elif txtID.get() == 'user' and txtPass.get() == 'user':  # placeholder
        sc.destroy()
        userScreen()
    elif txtID.get() == '' or txtPass.get() == '':
        messagebox.showerror('Login Failed', 'Provide an Account ID or Password')
    else:
        messagebox.showerror('Login Failed', 'Invalid Account ID or Password')
        txtID.delete(0, END) #Empties the entry box
        txtPass.delete(0, END)

# Function to switch between frames
def openFrame(frame):
    frame.tkraise()

# Universal Back Function
def logout(screen):
    screen.destroy()
    loginScreen()
    
def back(mainFr):
    mainFr.tkraise()

def createAcc(user, screen):
    """Opens window to create new accounts"""
    # Check for empty fields except ID
    for key, value in user.items():
        if key != 'ID' and not value.strip():  # Skips ID field
            messagebox.showerror('Error', f'{key} field cannot be empty.')
            return
        
    if user['ID']:
        if not user['ID'].isdigit() or len(user['ID']) != 9:
            messagebox.showerror('Error', 'Invalid account ID provided.')
            return

    # Field-specific validation
    if not user['First Name'].isalpha():
        messagebox.showerror('Error', 'First name must contain only letters.')
        return

    if not user['Last Name'].isalpha():
        messagebox.showerror('Error', 'Last name must contain only letters.')
        return

    if not user['Phone Number'].isdigit() or len(user['Phone Number']) != 11:
        messagebox.showerror('Error', 'Contact number must be exactly 11 digits.')
        return

    if '@' not in user['Email'] or '.' not in user['Email']:
        messagebox.showerror('Error', 'Invalid email format.')
        return

    try:
        balance = float(user['Balance'])
        if balance < 0:
            messagebox.showerror('Error', 'Balance cannot be negative.')
            return
    except ValueError:
        messagebox.showerror('Error', 'Balance must be a valid number.')
        return

    if len(user['Password']) < 6:
        messagebox.showerror('Error', 'Password must be at least 6 characters long.')
        return

    # Confirm before creating new account
    if messagebox.askokcancel('Confirm', 'Are all details correct?'):
        # bank.createAccount(
        # user['fname'], user['lname'], float(user['balance']), 
        # user['num'], user['email'], user['pass'])
        messagebox.showinfo('Success', 'Account successfully created!\nYour account number is: ')
        screen.destroy()
    else:
        userScreen()
        return
        
def submit(fields, screen):
    """Combines all fields into a single dictionary"""
    accountDetails = {key: entry.get().strip() for key, entry in fields.items()}
    createAcc(accountDetails, screen)

def createWindow():
    """Window for creating new accounts"""
    scCreate = Toplevel()
    scCreate.title('Create Account')
    scCreate.geometry('800x600')
    scCreate.resizable(False, False)
    scCreate.grab_set() # Ensures login window cannot be accessed while this is active

    lblFont = ('Arial', 18, 'bold')
    txtFont = ('Arial', 18)
    btnFont = ('Arial', 16)

    # Labels
    lblHeader = Label(scCreate, text='Enter user details', font=('Arial', 20, 'bold'))
    lblID = Label(scCreate, text='Account ID:', font=lblFont)
    lblFname = Label(scCreate, text='First Name:', font=lblFont)
    lblLname = Label(scCreate, text='Last Name:', font=lblFont)
    lblNum = Label(scCreate, text='Contact Number:', font=lblFont)
    lblEmail = Label(scCreate, text='Email:', font=lblFont)
    lblBalance = Label(scCreate, text='Balance:', font=lblFont)
    lblPass = Label(scCreate, text='Password:', font=lblFont)

    # Entries
    txtID = Entry(scCreate, font=txtFont)
    txtFname = Entry(scCreate, font=txtFont)
    txtLname = Entry(scCreate, font=txtFont)
    txtNum = Entry(scCreate, font=txtFont)
    txtEmail = Entry(scCreate, font=txtFont)
    txtBalance = Entry(scCreate, font=txtFont)
    txtPass = Entry(scCreate, font=txtFont)

    fields = {
        'ID': txtID,
        'First Name': txtFname,
        'Last Name': txtLname,
        'Phone Number': txtNum,
        'Email': txtEmail,
        'Balance': txtBalance,
        'Password': txtPass
    }

    # Buttons
    btnCreate = Button(scCreate, text='Submit', font=btnFont, command=lambda: submit(fields, scCreate))
    btnCancel = Button(scCreate, text='Cancel', font=btnFont, command=scCreate.destroy)

    # Grid Layout
    lblHeader.grid(row=0, column=0, columnspan=2, pady=10)

    lblID.grid(row=1, column=0, sticky='w', padx=20, pady=5)
    txtID.grid(row=1, column=1, padx=20, pady=5)

    lblFname.grid(row=2, column=0, sticky='w', padx=20, pady=5)
    txtFname.grid(row=2, column=1, padx=20, pady=5)

    lblLname.grid(row=3, column=0, sticky='w', padx=20, pady=5)
    txtLname.grid(row=3, column=1, padx=20, pady=5)

    lblNum.grid(row=4, column=0, sticky='w', padx=20, pady=5)
    txtNum.grid(row=4, column=1, padx=20, pady=5)

    lblEmail.grid(row=5, column=0, sticky='w', padx=20, pady=5)
    txtEmail.grid(row=5, column=1, padx=20, pady=5)

    lblBalance.grid(row=6, column=0, sticky='w', padx=20, pady=5)
    txtBalance.grid(row=6, column=1, padx=20, pady=5)

    lblPass.grid(row=7, column=0, sticky='w', padx=20, pady=5)
    txtPass.grid(row=7, column=1, padx=20, pady=5)

    btnCreate.grid(row=8, column=0, pady=20)
    btnCancel.grid(row=8, column=1, pady=20)
    
def userScreen():
    """Ordinary user main menu"""
    userSc = Tk()
    logo = PhotoImage(file='Tam-Bank/GUI/logo.png')
    titleLogo = PhotoImage(file='Tam-Bank/GUI/TamBank.png')
    userSc.title('TamBank - User Screen')
    userSc.geometry('1024x768')
    userSc.config(bg='white')
    
    btnFont = ('Helvetica', 15, 'bold')

    header = Frame(userSc, bg='white', width=1024, height=200)
    header.grid(row=0, column=0, sticky="ew")
    lblHeader = Label(header, image=titleLogo, bg='white')
    lblHeader.place(relx=0.5, rely=0.5, anchor='center')

    userBody = Frame(userSc, bg='white')
    userBody.grid(row=1, column=0, sticky="nsew")

    frmView = Frame(userSc, bg='white')
    frmView.grid(row=1, column=0, sticky="nsew")
    
    frmDeposit = Frame(userSc, bg='white')
    frmDeposit.grid(row=1, column=0, sticky="nsew")
    
    frmWithdraw = Frame(userSc, bg='white')
    frmWithdraw.grid(row=1, column=0, sticky="nsew")
    
    frmTransfer = Frame(userSc, bg='white')
    frmTransfer.grid(row=1, column=0, sticky="nsew")
    
    frmPass = Frame(userSc, bg='white')
    frmPass.grid(row=1, column=0, sticky="nsew")

    frmClose = Frame(userSc, bg='white')
    frmClose.grid(row=1, column=0, sticky="nsew")

    btnView = Button(userBody, text='View Account', width=15, height=5, font=btnFont, command=lambda: openFrame(frmView))
    btnDeposit = Button(userBody, text='Deposit', width=15, height=5, font=btnFont, command=lambda: openFrame(frmDeposit))
    btnWithdraw = Button(userBody, text='Withdraw', width=15, height=5, font=btnFont, command=lambda: openFrame(frmWithdraw))
    btnTransfer = Button(userBody, text='Transfer', width=15, height=5, font=btnFont, command=lambda: openFrame(frmTransfer))
    btnChangePass = Button(userBody, text='Change Password', width=15, height=5, font=btnFont, command=lambda: openFrame(frmPass))
    btnClose = Button(userBody, text='Close Account', width=15, height=5, font=btnFont, command=lambda: openFrame(frmClose))

    # Operations positions
    btnView.grid(row=0, column=0, padx=10, pady=10)
    btnDeposit.grid(row=0, column=1, padx=10, pady=10)
    btnWithdraw.grid(row=1, column=0, padx=10, pady=10)
    btnTransfer.grid(row=1, column=1, padx=10, pady=10)
    btnChangePass.grid(row=2, column=0, padx=10, pady=10)
    btnClose.grid(row=2, column=1, padx=10, pady=10)
    
    # Back buttons
    btnBackView = Button(frmView, text="Back", font=btnFont, command=lambda: openFrame(userBody))
    btnBackDepo = Button(frmDeposit, text="Back", font=btnFont, command=lambda: openFrame(userBody))
    btnBackWith = Button(frmWithdraw, text="Back", font=btnFont, command=lambda: openFrame(userBody))
    btnBackTrans = Button(frmTransfer, text="Back", font=btnFont, command=lambda: openFrame(userBody))
    btnBackPass = Button(frmPass, text="Back", font=btnFont, command=lambda: openFrame(userBody))
    btnBackClose = Button(frmClose, text="Back", font=btnFont, command=lambda: openFrame(userBody))
    
    # Back buttons positions
    btnBackView.pack(pady=20)
    btnBackDepo.pack(pady=20)
    btnBackWith.pack(pady=20)
    btnBackTrans.pack(pady=20)
    btnBackPass.pack(pady=20)
    btnBackClose.pack(pady=20)

    btnLogout = Button(userBody, text="Log out", font=btnFont, command=lambda: logout(userSc))
    btnLogout.grid(row=3, column=0, columnspan=2, pady=20)

    openFrame(userBody)
    userBody.mainloop()

# **Admin Screen**
def adminScreen():
    sc = Tk()
    logo = PhotoImage(file='Tam-Bank/GUI/logo.png')
    titleLogo = PhotoImage(file='Tam-Bank/GUI/TamBank.png')
    sc.title('TamBank Admin')
    sc.geometry('1024x768')
    sc.config(bg='white')
    
    btnFont = ('Helvetica', 15, 'bold')

    header = Frame(sc, bg='white', width=1024, height=200)
    header.grid(row=0, column=0, sticky="ew")
    lblHeader = Label(header, image=titleLogo, bg='white')
    lblHeader.place(relx=0.5, rely=0.5, anchor='center')

    adminBody = Frame(sc, bg='white')
    adminBody.grid(row=1, column=0, sticky="nsew")

    frmView = Frame(sc, bg='white')
    frmView.grid(row=1, column=0, sticky="nsew")

    frmUpdate = Frame(sc, bg='white')
    frmUpdate.grid(row=1, column=0, sticky="nsew")
    
    frmDelete = Frame(sc, bg='white')
    frmDelete.grid(row=1, column=0, sticky="nsew")

    btnView = Button(adminBody, text='View Account', width=15, height=5, font=btnFont, command=lambda: openFrame(frmView))
    btnUpdate = Button(adminBody, text='Update Account', width=15, height=5, font=btnFont, command=lambda: openFrame(frmUpdate))
    btnDelete = Button(adminBody, text='Delete Account', width=15, height=5, font=btnFont, command=lambda: openFrame(frmDelete))
    btnBackView = Button(frmView, text="Back", font=btnFont, command=lambda: openFrame(adminBody))
    btnBackUpdate = Button(frmUpdate, text="Back", font=btnFont, command=lambda: openFrame(adminBody))
    btnBackDelete = Button(frmDelete, text="Back", font=btnFont, command=lambda: openFrame(adminBody))
    
    # Back button positions
    btnBackView.pack(pady=20)
    btnBackUpdate.pack(pady=20)
    btnBackDelete.pack(pady=20)


    btnView.grid(row=0, column=0, padx=10, pady=10)
    btnUpdate.grid(row=0, column=1, padx=10, pady=10)
    btnDelete.grid(row=1, column=0, padx=10, pady=10)

    btnLogout = Button(adminBody, text="Log Out", font=btnFont, command=lambda: logout(sc))
    btnLogout.grid(row=3, column=0, columnspan=2, pady=20)

    openFrame(adminBody)
    sc.mainloop()


def loginScreen():
    """First screen to authenticate users"""
    sc = Tk()
    #Login Screen Settings
    mainTitle = 'TamBank'
    logo = PhotoImage(file = 'Tam-Bank/GUI/logo.png')
    titleLogo = PhotoImage(file = 'Tam-Bank/GUI/TamBank.png')
    sc.title(mainTitle)
    sc.geometry("800x600+400+100")
    sc.iconphoto(True, logo)
    sc.resizable(False,False)
    
    defaultFont = ('Helvetica', 20, 'bold')
    btnFont = ('Helvetica', 12, 'bold')
    

    lblTitle = Label(sc, image = titleLogo)
    lblAccountID = Label(sc, text = 'Account ID:', font = defaultFont)
    lblPassword = Label(sc, text = 'Password:', font = defaultFont)
    txtID = Entry(sc, font = defaultFont)
    txtPass = Entry(sc, font = defaultFont, show= '*')
    btnLogin = Button(sc, text = 'Login', font = btnFont, padx = 15, command = lambda: authenticate(sc, txtID, txtPass))
    btnRegister = Button(sc, text = 'Register', font = btnFont, padx = 15, command = lambda: createWindow())
    lblTitle.pack(pady = 100)
    lblAccountID.place(x = 160, y = 300)
    lblPassword.place(x = 175, y = 350)
    txtID.place(x = 340, y = 300)
    txtPass.place(x = 340, y = 350)
    btnLogin.place(x = 450, y = 400)
    btnRegister.place(x = 555, y = 400)


    sc.mainloop()

loginScreen()