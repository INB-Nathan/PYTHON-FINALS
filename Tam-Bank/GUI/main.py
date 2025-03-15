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

def createAcc():
    print('creating acc...')
    
def viewAcc():
    print('view acc...')
    
def updateAcc():
    print('udpate acc...')
    
def deleteAcc():
    print('delete acc...')

def deposit():
    print('deposit acc...')
    
def withdraw():
    print('withdraw acc...')
    
def transfer():
    print('transfer acc...')
    
def changePass():
    print('change pass acc...')
   


def userScreen():
    """Opens new window for account management"""
    sc = Tk()
    logo = PhotoImage(file='logo.png')
    titleLogo = PhotoImage(file='TamBank.png')
    sc.title('TamBank')
    sc.geometry("1024x768+530+150")
    sc.iconphoto(True, logo)
    sc.resizable(False, False)
    sc.config(bg='white')

    btnFont = ('Helvetica', 15, 'bold')

    # Header
    header = Frame(sc, bg='white', width=1024, height=200)
    lblHeader = Label(header, image=titleLogo, bg='white')

    # Menu Frame (Fixed Size)
    body = Frame(sc, bg='white', width=1024, height=568)

    # Buttons
    btnCreate = Button(body, text='Create Account', width=15, height=5, font=btnFont, command=createAcc)
    btnView = Button(body, text='View Account', width=15, height=5, font=btnFont, command=viewAcc)
    btnUpdate = Button(body, text='Update Account', width=15, height=5, font=btnFont, command=updateAcc)
    btnDelete = Button(body, text='Delete Account', width=15, height=5, font=btnFont, command=deleteAcc)
    btnDeposit = Button(body, text='Deposit', width=15, height=5, font=btnFont, command=deposit)
    btnWithdraw = Button(body, text='Withdraw', width=15, height=5, font=btnFont, command=withdraw)
    btnTransfer = Button(body, text='Transfer', width=15, height=5, font=btnFont, command=transfer)
    btnChangePass = Button(body, text='Change Password', width=15, height=5, font=btnFont, command= changePass)

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
    logo = PhotoImage(file = 'logo.png')
    titleLogo = PhotoImage(file = 'TamBank.png')
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
loginScreen()
