from tkinter import *
from tkinter import messagebox  # for pop-up message windows




def authenticate(sc, txtID, txtPass):
    """Validates login and opens corresponding screen if credentials match."""
    if txtID.get() == 'admin' and txtPass.get() == 'admin':  # placeholder
        sc.destroy()
        userScreen()
    elif txtID.get() == '' or txtPass.get() == '':
        messagebox.showerror('Login Failed', 'Provide an Account ID or Password')
    else:
        messagebox.showerror('Login Failed', 'Invalid Account ID or Password')
        txtID.delete(0, END) #Empties the entry box
        txtPass.delete(0, END)

def createAcc(user):
    """Opens window to create new accounts"""
    # Check for empty fields except 'id'
    for key, value in user.items():
        if key != 'id' and not value.strip():  # Skips ID field
            messagebox.showerror('Error', f'{key} field cannot be empty.')
            return
        
    if user['id']:
        if not user['id'].isdigit() or len(user['id']) != 9:
            messagebox.showerror('Error', 'Invalid account ID provided.')
            return

    # Field-specific validation
    if not user['fname'].isalpha():
        messagebox.showerror('Error', 'First name must contain only letters.')
        return

    if not user['lname'].isalpha():
        messagebox.showerror('Error', 'Last name must contain only letters.')
        return

    if not user['num'].isdigit() or len(user['num']) != 11:
        messagebox.showerror('Error', 'Contact number must be exactly 11 digits.')
        return

    if '@' not in user['email'] or '.' not in user['email']:
        messagebox.showerror('Error', 'Invalid email format.')
        return

    try:
        balance = float(user['balance'])
        if balance < 0:
            messagebox.showerror('Error', 'Balance cannot be negative.')
            return
    except ValueError:
        messagebox.showerror('Error', 'Balance must be a valid number.')
        return

    if len(user['pass']) < 6:
        messagebox.showerror('Error', 'Password must be at least 6 characters long.')
        return

    # Confirm before creating new account
    if messagebox.askokcancel('Confirm', 'Are all details correct?'):
        # bank.createAccount(
        # user['fname'], user['lname'], float(user['balance']), 
        # user['num'], user['email'], user['pass'])
        messagebox.showinfo('Success', 'Account successfully created!')
    else:
        return
        

def submit(fields):
    """Combines all fields into a single dictioinary"""
    accountDetails = {key: entry.get().strip() for key, entry in fields.items()}
    createAcc(accountDetails)

def createWindow():
    """Window for creating new accounts"""
    scCreate = Toplevel()
    scCreate.title('Create Account')
    scCreate.geometry('800x600')
    scCreate.resizable(False, False)
    scCreate.grab_set()
    scCreate.lift()

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
    btnCreate = Button(scCreate, text='Submit', font=btnFont, command=lambda: submit(fields))
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

def viewWindow():
    print('view acc...')

def updateWindow():
    print('update acc...')

def deleteWindow():
    print('delete acc...')

def depositWindow():
    print('deposit acc...')

def withdrawWindow():
    print('withdraw acc...')

def transferWindow():
    print('transfer acc...')

def changePassWindow():
    print('change pass acc...')

def userScreen():
    """Main menu after successful login"""
    sc = Tk()
    logo = PhotoImage(file='Tam-Bank/GUI/logo.png')
    titleLogo = PhotoImage(file='Tam-Bank/GUI/TamBank.png')
    sc.title('TamBank')
    sc.geometry('1024x768')
    sc.iconphoto(True, logo)
    sc.resizable(False, False)
    sc.config(bg='white')

    btnFont = ('Helvetica', 15, 'bold')

    # Header
    header = Frame(sc, bg='white', width=1024, height=200)
    lblHeader = Label(header, image=titleLogo, bg='white')

    # Body
    body = Frame(sc, bg='white', width=1024, height=568)

    # Buttons
    btnCreate = Button(body, text='Create Account', width=15, height=5, font=btnFont, command=createWindow)
    btnView = Button(body, text='View Account', width=15, height=5, font=btnFont, command=viewWindow)
    btnUpdate = Button(body, text='Update Account', width=15, height=5, font=btnFont, command=updateWindow)
    btnDelete = Button(body, text='Delete Account', width=15, height=5, font=btnFont, command=deleteWindow)
    btnDeposit = Button(body, text='Deposit', width=15, height=5, font=btnFont, command=depositWindow)
    btnWithdraw = Button(body, text='Withdraw', width=15, height=5, font=btnFont, command=withdrawWindow)
    btnTransfer = Button(body, text='Transfer', width=15, height=5, font=btnFont, command=transferWindow)
    btnChangePass = Button(body, text='Change Password', width=15, height=5, font=btnFont, command=changePassWindow)

    header.grid(row=0, column=0, rowspan=2, sticky='ew')
    lblHeader.place(relx=0.5, rely=0.5, anchor='center')

    body.grid(row=5, column=0)

    # Arrange Buttons in Grid (Fixed Position)
    btnCreate.grid(row=0, column=0, padx=10, pady=10)
    btnView.grid(row=0, column=1, padx=10, pady=10)
    btnUpdate.grid(row=0, column=2, padx=10, pady=10)
    btnDelete.grid(row=1, column=0, padx=10, pady=10)
    btnDeposit.grid(row=1, column=1, padx=10, pady=10)
    btnWithdraw.grid(row=1, column=2, padx=10, pady=10)
    btnTransfer.grid(row=2, column=0, padx=10, pady=10)
    btnChangePass.grid(row=2, column=1, padx=10, pady=10)

    sc.mainloop()

def loginScreen():
    """First screen to authenticate users"""
    sc = Tk()
    
    #Login Screen Settings
    mainTitle = 'TamBank'
    logo = PhotoImage(file = 'Tam-Bank/GUI/logo.png')
    titleLogo = PhotoImage(file = 'Tam-Bank/GUI/TamBank.png')
    sc.title(mainTitle)
    sc.geometry("800x600+600+200")
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
    
    lblTitle.pack(pady = 100)
    lblAccountID.place(x = 160, y = 300)
    lblPassword.place(x = 175, y = 350)
    txtID.place(x = 340, y = 300)
    txtPass.place(x = 340, y = 350)
    btnLogin.place(x = 555, y = 400)


    sc.mainloop()
    
    
#-------------MAIN---------------
# loginScreen() disabled for bypass muna
userScreen()