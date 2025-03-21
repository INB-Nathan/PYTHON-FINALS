from tkinter import *
from tkinter import messagebox, ttk
import datetime

class AdminGUIinterface:
    """ Admin GUI Interface """

    def __init__(self, bank):
        """ Initializer """
        pass

    def start(self):
        """ Start the GUI """
        pass

    def _setupAccounts(self):
        """ Setup the accounts """
        pass

    def _loadAccounts(self):
        """ Load the accounts """
        pass

    def _setupTransactions(self):
        """ Setup the transactions """
        pass

    def _setupSystem(self):
        """ Setup the system """
        pass

    def _viewAccount(self):
        """ View the account """
        pass

    def _editAccount(self, fields):
        """ Edit the account """
        try:
            for field, entry in fields.items():
                if not entry.get().strip():
                    messagebox.showerror('Error', f'{field} field cannot be empty.')
                    return

            accountID = fields['Account ID'].get().strip()
            fName = fields['First Name'].get()
            lName = fields['Last Name'].get()
            mobileNo = fields['Phone Number'].get()
            email = fields['Email'].get()
            
            # Validate account ID
            if not accountID.isdigit():
                messagebox.showerror('Error', 'Invalid account ID. It should contain only numbers.')
                return

            accountID = int(accountID)  # Convert to integer

            if not (20210000 <= accountID <= 20230000):
                messagebox.showerror('Error', 'Invalid account ID. It should be between 20210000 and 20230000.')
                return

            # phone number validation
            if not (mobileNo.isdigit() and mobileNo.startswith('09') and len(mobileNo) == 11):
                messagebox.showerror('Error', 'Invalid phone number. It should start with 09 and have 11 digits.')
                return

            # email validation
            if '@' not in email or '.' not in email:
                messagebox.showerror('Error', 'Invalid email format.')
                return

            success, message = self.bank.updateAccount(fName, lName, mobileNo, email, accountID)

            if success:
                messagebox.showinfo('Success', 'Account successfully updated!')
            else:
                messagebox.showerror('Error', message)

        except Exception as e:
            messagebox.showerror('Error', f'Failed to update account: {str(e)}')
            print(f"Exception occurred: {e}")

    def _editDetails(self):
        """ edit account from details window """
        pass

    def _editForm(self):
        """ Edit form """
        pass

    def _saveAccountChanges(self):
        """ Save the account changes """
        pass

    def _deleteAccount(self):
        """ Delete the account """
        pass

    def _loadTransactions(self):
        """ Load the transactions """
        pass

    def _searchAccount(self):
        """ Search the account """
        pass

    def _changeAdminPassword(self):
        """ Change the admin password """
        pass

    def _logout(self):
        """ Logout """
        pass

    def _setupUpdateDetails(self, frame):
        """ Display update account """
        header = Label(frame, text='Update Account', font=('Helvetica', 24, 'bold'))
        header.pack(pady=20)

        updateFrame = Frame(frame)
        updateFrame.pack(pady=20, fill=X, padx=50)

        fields = {}

        # Function to fetch account details when ID is entered
        def fetchDetails(event):
            accountID = accountIDEntry.get().strip()
            if accountID.isdigit() and 20210000 <= int(accountID) <= 20230000:
                account = self.bank.getAccount(int(accountID))
                if account:
                    fields["First Name"].delete(0, END)
                    fields["First Name"].insert(0, account.fName)

                    fields["Last Name"].delete(0, END)
                    fields["Last Name"].insert(0, account.lName)

                    fields["Phone Number"].delete(0, END)
                    fields["Phone Number"].insert(0, account.mobileNo)

                    fields["Email"].delete(0, END)
                    fields["Email"].insert(0, account.email)
                else:
                    messagebox.showerror("Error", "Account not found!")
            else:
                messagebox.showerror("Error", "Invalid Account ID! Must be between 20210000 and 20230000.")

        # Account ID Field
        rowFrame = Frame(updateFrame)
        rowFrame.pack(fill=X, pady=5)

        label = Label(rowFrame, text="Account ID:", font=('Helvetica', 14, 'bold'), width=15, anchor='w')
        label.pack(side=LEFT)

        accountIDEntry = Entry(rowFrame, font=('Helvetica', 14))
        accountIDEntry.pack(side=LEFT, padx=10, fill=X, expand=True)
        accountIDEntry.bind("<Return>", fetchDetails)  # Press Enter to fetch details
        
        fields["Account ID"] = accountIDEntry

        # Other account fields
        field_data = [
            ('First Name', ''),
            ('Last Name', ''),
            ('Phone Number', ''),
            ('Email', '')
        ]

        for labelText, value in field_data:
            rowFrame = Frame(updateFrame)
            rowFrame.pack(fill=X, pady=5)

            label = Label(rowFrame, text=f"{labelText}:", font=('Helvetica', 14, 'bold'), width=15, anchor='w')
            label.pack(side=LEFT)

            entry = Entry(rowFrame, font=('Helvetica', 14))
            entry.pack(side=LEFT, padx=10, fill=X, expand=True)

            fields[labelText] = entry  # Store in fields dictionary

        btnFrame = Frame(updateFrame)
        btnFrame.pack(pady=20)

        btnUpdate = Button(btnFrame, text='Update', font=('Helvetica', 12),
                        command=lambda: self._editAccount(fields))
        
        btnUpdate.pack(side=LEFT, padx=10)