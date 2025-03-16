from tkinter import *
from tkinter import messagebox #for pop-up message windows




def authenticate(sc, txtID, txtPass):
    """Validates login and opens corresponding screen if credentials match."""
    if txtID.get() == "admin" and txtPass.get() == "admin": #--------- place holder 
        sc.destroy()  
        userScreen()
    elif txtID.get() == "" or txtPass.get() == "":
        messagebox.showerror("Login Failed", "Provide an Account ID or Password")
    else:
        messagebox.showerror("Login Failed", "Invalid Account ID or Password")
        txtID.delete(0, END)
        txtPass.delete(0, END)

def createWindow():
    """Opens window to create new accounts"""
    scCreate = Toplevel() # scCreate is placed on top of the main window
    scCreate.title('Create Account') # Title of the window
    scCreate.geometry("800x600") # Window size
    scCreate.resizable(False, False) # Disables resize
    scCreate.grab_set() # Ensures all action is applied to the current window not the user window

    lblFont = ('Arial', 18, 'bold')
    txtFont = ('Arial', 18)
    btnFont = ("Arial", 16)

    # Labels
    lblHeader = Label(scCreate, text="Enter user details", font=("Arial", 20, 'bold'))
    lblID = Label(scCreate, text="Account ID:", font = lblFont)
    lblFname = Label(scCreate, text="First Name: ", font = lblFont)
    lblLname = Label(scCreate, text="Last Name", font = lblFont)
    lblNum = Label(scCreate, text="Contact Number:", font = lblFont)

    # Entries
    txtID = Entry(scCreate, font=txtFont)
    txtFname = Entry(scCreate, font=txtFont)
    txtLname = Entry(scCreate, font=txtFont)
    txtNum = Entry(scCreate, font=txtFont)

    # Buttons
    btnCreate = Button(scCreate, text='Create', font = btnFont, command = lambda: print('Created Acc')) # will be replaced with the real func
    btnCancel = Button(scCreate, text="Cancel", font= btnFont, command=scCreate.destroy)

    # Used grid for table positioning
    lblHeader.grid(row=0, column=0, columnspan=2, pady=10) #pady or padx is for padding
    
    lblID.grid(row=1, column=0, sticky="w", padx=20, pady=5) #sticky acts like justify 'w' means west 
    txtID.grid(row=1, column=1, padx=20, pady=5)

    lblFname.grid(row=2, column=0, sticky="w", padx=20, pady=5)
    txtFname.grid(row=2, column=1, padx=20, pady=5)

    lblLname.grid(row=3, column=0, sticky="w", padx=20, pady=5)
    txtLname.grid(row=3, column=1, padx=20, pady=5)

    lblNum.grid(row=4, column=0, sticky="w", padx=20, pady=5)
    txtNum.grid(row=4, column=1, padx=20, pady=5)

    btnCreate.grid(row=5, column=0, pady=20)
    btnCancel.grid(row=5, column=1, pady=20)

    #no need for main loop because this is a child window
    
    
def viewWindow():
    print('view acc...')
    
def updateWindow():
    print('udpate acc...')
    
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
    """Opens new window for account management"""
    sc = Tk()
    logo = PhotoImage(file = 'Tam-Bank/GUI/logo.png')
    titleLogo = PhotoImage(file = 'Tam-Bank/GUI/TamBank.png')
    sc.title('TamBank')
    sc.geometry("1024x768")
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
    btnDeposit = Button(body, text='Deposit', width=15, height=5, font=btnFont, command = depositWindow)
    btnWithdraw = Button(body, text='Withdraw', width=15, height=5, font=btnFont, command=withdrawWindow)
    btnTransfer = Button(body, text='Transfer', width=15, height=5, font=btnFont, command=transferWindow)
    btnChangePass = Button(body, text='Change Password', width=15, height=5, font=btnFont, command= changePassWindow)

    # Grid Layout
    header.grid(row=0, column=0, rowspan= 2, sticky="ew")
    lblHeader.place(relx=0.5, rely=0.5, anchor="center")

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
