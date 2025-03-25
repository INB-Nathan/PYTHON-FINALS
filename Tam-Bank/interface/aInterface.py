from tkinter import *
from tkinter import messagebox, ttk
import datetime

class AdminGUIinterface:
    """Admin GUI interface for managing the banking system"""
    
    def __init__(self, bankService):
        self.bank = bankService
        self.mainWindow = None
        
    def start(self, username="admin"):
        """Start the admin interface with the given username"""
        self.mainWindow = Tk()
        self.mainWindow.title("TamBank - Admin Panel")
        self.mainWindow.geometry("1024x768")
        
        try:
            self.logo = PhotoImage(file = 'Tam-Bank/graphics/logo.png')
            self.titleLogo = PhotoImage(file = 'Tam-Bank/graphics/TamBank.png')
            self.mainWindow.iconphoto(True, self.logo)
        except:
            self.titleLogo = None
        
        # reload accounts
        accounts = self.bank.getAllAccounts()
        
        # Header frame with admin info and formatted date/time
        headerFrame = Frame(self.mainWindow, bg="#333333", height=60)
        headerFrame.pack(fill=X)
        
        # Information Bar
        self.userLabel = Label(headerFrame, 
                            text=f"{username}", 
                            font=('Helvetica', 12), 
                            bg="#333333", fg="white")
        self.userLabel.pack(side=LEFT, padx=20, pady=10)
        
        self.timeLabel = Label(headerFrame, 
                            text="", 
                            font=('Helvetica', 12), 
                            bg="#333333", fg="white")
        self.timeLabel.pack(side=RIGHT, padx=20, pady=10)

        self._updateClock()
        
        # Nav Bar
        style = ttk.Style() 
        style.configure('TNotebook.Tab', font=('Helvetica','12'))
        tabControl = ttk.Notebook(self.mainWindow)
        accountsTab = Frame(tabControl)
        applicationsTab = Frame(tabControl)
        transactionsTab = Frame(tabControl)
        systemTab = Frame(tabControl)
        tabControl.add(accountsTab, text="Account Management")
        tabControl.add(transactionsTab, text="Transaction History")
        tabControl.add(applicationsTab, text = "Applications")
        tabControl.add(systemTab, text="System")
        tabControl.pack(expand=1, fill=BOTH)
        self._setupAccountsTab(accountsTab)
        self._setupTransactionsTab(transactionsTab)
        self._setupApplicationsTab(applicationsTab)
        self._setupSystemTab(systemTab)
        
        # Footer logout
        footerFrame = Frame(self.mainWindow)
        footerFrame.pack(fill=X, side=BOTTOM)
        
        logoutBtn = Button(footerFrame, text="Logout", command=self._logout,
                          font=('Helvetica', 12), padx=20, pady=5)
        logoutBtn.pack(side=RIGHT, padx=20, pady=10)
        
        self.mainWindow.mainloop()

    def _setupApplicationsTab(self,frame):
        """ set up for application tab """
        header = Label(frame, text = 'Applications Management', font=('Helvetica', 18, 'bold'))
        header.pack(pady=20)

        filterFrame = Frame(frame)
        filterFrame.pack(fill = X, padx = 20, pady = 10)

        filterLabel = Label(filterFrame, text="Filter by status:", font=('Helvetica', 12))
        filterLabel.pack(side=LEFT, padx=5)

        statusVar = StringVar()
        statusVar.set('All')

        statusDropdown = ttk.Combobox(filterFrame, textvariable = statusVar,
                                      values = ["All", "Pending", "Accepted", "Declined"],
                                      state = "readonly", width = 15)
        statusDropdown.pack(side = LEFT, padx=5)

        filterBtn = Button(filterFrame, text = "Apply Filter", font = ('Helvetica', 12),
                           command = lambda: self._loadApplications(applicationsTree, statusVar.get()))
        filterBtn.pack(side = LEFT, padx = 5)

        refreshBtn = Button(filterFrame, text = "Refresh" , font=('Helvetica', 12),
                            command = lambda: self._loadApplications(applicationsTree, statusVar.get()))
        refreshBtn.pack(side= LEFT, padx = 5)

        treeFrame = Frame(frame)
        treeFrame.pack(fill=BOTH, expand = True, padx = 20, pady = 10)
        
        columns = ('application_id', 'name', 'bank_type', 'status', 'date')
        applicationsTree = ttk.Treeview(treeFrame, columns=columns, show='headings')

        applicationsTree.heading('application_id', text = 'Application ID')
        applicationsTree.heading('name', text = 'Applicant Name')
        applicationsTree.heading('bank_type', text = 'Account Type')
        applicationsTree.heading('status', text = 'Status')
        applicationsTree.heading('date', text = 'Application Date')

        applicationsTree.column('application_id', width = 150)
        applicationsTree.column('name', width = 200)
        applicationsTree.column('bank_type', width = 120)
        applicationsTree.column('status', width = 100)
        applicationsTree.column('date', width=150)

        yScrollBar = ttk.Scrollbar(treeFrame, orient=VERTICAL, command = applicationsTree.yview)
        applicationsTree.configure(yscrollcommand=yScrollBar.set)

        applicationsTree.pack(side=LEFT, fill=BOTH, expand=True)
        yScrollBar.pack(side=RIGHT, fill=Y)

        applicationsTree.bind('<Double-1>', lambda e: self._viewApplicationDetails(applicationsTree))

        actionsFrame = Frame(frame)
        actionsFrame.pack(fill=X, padx=20, pady=10)

        viewBtn = Button(actionsFrame, text="View Details", font = ('Helvetica', 12), command= lambda: self._viewApplicationDetails(applicationsTree))
        viewBtn.pack(side=LEFT, padx = 5)
        approveBtn = Button(actionsFrame, text="Approve Application", font = ('Helvetica', 12),bg='#4CAF50', fg='white', command= lambda: self._approveApplication(applicationsTree))
        approveBtn.pack(side = LEFT, padx= 5)
        declineBtn = Button(actionsFrame, text="Decline Application", font = ('Helvetica', 12),bg = '#f44336',fg = 'white', command= lambda: self._declineApplication(applicationsTree))
        declineBtn.pack(side = LEFT, padx= 5)

        self._loadApplications(applicationsTree)

    def _loadApplications(self, tree, statusFilter = "ALL"):
        """ Load applications """
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            from utils.filehandling import fileHandling
            
            # Load all applications
            applications = fileHandling.loadApplications()
            
            # Filter by status if needed
            if statusFilter != "All":
                applications = [app for app in applications if app['status'] == statusFilter]
            
            if not applications:
                tree.insert('', 'end', values=('', 'No applications found', '', '', ''))
                return
            
            # Custom coloring based on status
            tree.tag_configure('pending', background='#fff9c4')
            tree.tag_configure('accepted', background='#c8e6c9')
            tree.tag_configure('declined', background='#ffcdd2')
            
            for app in applications:
                name = f"{app['fName']} {app['lName']}"
                date = app['applicationDate'].strftime("%Y-%m-%d %H:%M:%S")
                
                item_id = tree.insert('', 'end', values=(
                    app['applicationId'],
                    name,
                    app['bankType'],
                    app['status'],
                    date
                ))
                
                status_tag = app['status'].lower()
                if status_tag in ['pending', 'accepted', 'declined']:
                    tree.item(item_id, tags=(status_tag,))
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not load applications: {str(e)}")
            tree.insert('', 'end', values=('', f'Error: {str(e)}', '', '', ''))

    def _viewApplicationDetails(self, tree):
        """ view details of applicant """
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an application to view.")
            return

        application_ID= tree.item(selected[0])['values'][0]

        try:
            from utils.filehandling import fileHandling
            applications = fileHandling.loadApplications()

            application = None
            for app in applications:
                if app['applicationId'] == application_ID:
                    application = app
                    break
            
            if not application:
                messagebox.showerror("Error", f"Application {application_ID} not found")
                return

            detailWindow = Toplevel(self.mainWindow)
            detailWindow.title(f"Application Details - {application_ID}")
            detailWindow.geometry("500x400")
            detailWindow.grab_set()

            Label(detailWindow, text = "Application Details", font = ('Helvetica', 16 , 'bold'))

            detailsFrame = Frame(detailWindow)
            detailsFrame.pack(fill=BOTH, expand = True , padx=20, pady=10)

            fields = [
                ('Application ID', application['applicationId']),
                ('Full Name', f"{application['fName']} {application['lName']}"),
                ('Phone Number', application['mobileNo']),
                ('Email', application['email']),
                ('Initial Balance', f"PHP{application['initialBal']:.2f}"),
                ('Account Type', application['bankType']),
                ('Status', application['status']),
                ('Application Date', application['applicationDate'].strftime("%Y-%m-%d %H:%M:%S"))
            ]

            for i, (field, value) in enumerate(fields):
                Label(detailsFrame, text=field, font=('Helvetica', 12, 'bold')).grid(row=i, column=0, sticky=W, pady=5)
                Label(detailsFrame, text=value, font=('Helvetica', 12)).grid(row=i, column=1, sticky=W, pady=5)
            
            btnFrame = Frame(detailWindow)
            btnFrame.pack(fill=X, pady=10)
            
            if application['status'] == "Pending":
                approveBtn = Button(btnFrame, text="Approve", font=('Helvetica', 12),
                                bg='#4CAF50', fg='white',
                                command=lambda: self._processApplicationApproval(application, detailWindow, tree))
                approveBtn.pack(side=LEFT, padx=10)
                
                declineBtn = Button(btnFrame, text="Decline", font=('Helvetica', 12),
                                bg='#f44336', fg='white',
                                command=lambda: self._processApplicationDecline(application, detailWindow, tree))
                declineBtn.pack(side=LEFT, padx=10)
            
            closeBtn = Button(btnFrame, text="Close", font=('Helvetica', 12),
                            command=detailWindow.destroy)
            closeBtn.pack(side=RIGHT, padx=10)
    
        except Exception as e:
            messagebox.showerror("Error", f"Error viewing application: {str(e)}")

    def _approveApplication(self, tree):
        """Approve the selected application"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an application to approve")
            return
        
        app_id = tree.item(selected[0])['values'][0]
        status = tree.item(selected[0])['values'][3]
        
        if status != "Pending":
            messagebox.showwarning("Cannot Approve", "Only pending applications can be approved")
            return
        
        try:
            from utils.filehandling import fileHandling
            applications = fileHandling.loadApplications()
            
            application = None
            for app in applications:
                if app['applicationId'] == app_id:
                    application = app
                    break
            
            if not application:
                messagebox.showerror("Error", f"Application {app_id} not found")
                return
            
            self._processApplicationApproval(application, None, tree)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error approving application: {str(e)}")

    def _declineApplication(self, tree):
        """Decline the selected application"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an application to decline")
            return
        
        app_id = tree.item(selected[0])['values'][0]
        status = tree.item(selected[0])['values'][3]
        
        if status != "Pending":
            messagebox.showwarning("Cannot Decline", "Only pending applications can be declined")
            return
        
        try:
            from utils.filehandling import fileHandling
            applications = fileHandling.loadApplications()
            
            application = None
            for app in applications:
                if app['applicationId'] == app_id:
                    application = app
                    break
            
            if not application:
                messagebox.showerror("Error", f"Application {app_id} not found")
                return
            
            self._processApplicationDecline(application, None, tree)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error declining application: {str(e)}")

    def _processApplicationApproval(self, application, detailWindow=None, tree=None):
        """Process application approval and create new account"""
        confirm = messagebox.askyesno("Confirm Approval", 
                                f"Are you sure you want to approve this application from {application['fName']} {application['lName']}?\n\n"
                                f"This will create a new {application['bankType']} account.")
        
        if not confirm:
            return
        
        try:
            from utils.filehandling import fileHandling
            success, message = fileHandling.updateApplicationStatus(application['applicationId'], "Accepted")
            
            if not success:
                messagebox.showerror("Error", f"Failed to update application status: {message}")
                return
            
            defaultPin = 'TamBank123@!'
            account = self.bank.createAccount(
                application['fName'],
                application['lName'],
                application['initialBal'],
                application['mobileNo'],
                application['email'],
                defaultPin
            )
            
            if account:
                messagebox.showinfo("Success", 
                                f"Application approved successfully!\n\n"
                                f"New account created with ID: {account.accountNumber}\n\n"
                                f"Default PIN is set to: {defaultPin}\n\n"
                                f"Inform the customer to change their pin on login.")
                
                if detailWindow:
                    detailWindow.destroy()
                
                if tree:
                    self._loadApplications(tree)
                
                for tab in self.mainWindow.winfo_children():
                    if isinstance(tab, ttk.Notebook):
                        for tabId in tab.tabs():
                            tabName = tab.tab(tabId, "text")
                            if tabName == "Account Management":
                                tabFrame = self.mainWindow.nametowidget(tabId)
                                for widget in tabFrame.winfo_children():
                                    if isinstance(widget, Frame):
                                        for child in widget.winfo_children():
                                            if isinstance(child, ttk.Treeview):
                                                self._loadAccounts(child)
                                                break
                
                if hasattr(self, 'statsLabels'):
                    self._refreshSystemStats()
            else:
                messagebox.showerror("Error", "Failed to create account")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error processing approval: {str(e)}")

    def _processApplicationDecline(self, application, detailWindow=None, tree=None):
        """Process application decline"""
        confirm = messagebox.askyesno("Confirm Decline", 
                                f"Are you sure you want to decline this application from {application['fName']} {application['lName']}?")
        
        if not confirm:
            return
        
        try:
            # Update application status
            from utils.filehandling import fileHandling
            success, message = fileHandling.updateApplicationStatus(application['applicationId'], "Declined")
            
            if success:
                messagebox.showinfo("Success", "Application declined successfully")
                
                # Close detail window if it exists
                if detailWindow:
                    detailWindow.destroy()
                
                # Reload applications list
                if tree:
                    self._loadApplications(tree)
            else:
                messagebox.showerror("Error", f"Failed to update application status: {message}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error processing decline: {str(e)}")



    def _updateClock(self):
        """ Update clock every second """
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        self.timeLabel.config(text = f"Current Date and Time: {now}")
        self.mainWindow.after(1000, self._updateClock)
    
    def _setupAccountsTab(self, frame):
        """Set up the accounts management tab"""
        header = Label(frame, text="Account Management", font=('Helvetica', 18, 'bold'))
        header.pack(pady=20)
        
        searchFrame = Frame(frame)
        searchFrame.pack(fill=X, padx=20, pady=10)
        searchLabel = Label(searchFrame, text="Search accounts:", font=('Helvetica', 12))
        searchLabel.pack(side=LEFT, padx=5)
        searchEntry = Entry(searchFrame, font=('Helvetica', 12), width=30)
        searchEntry.pack(side=LEFT, padx=5)
        searchBtn = Button(searchFrame, text="Search", font=('Helvetica', 12),
                          command=lambda: self._searchAccounts(searchEntry.get(), accountsTree))
        searchBtn.pack(side=LEFT, padx=5)
        refreshBtn = Button(searchFrame, text="Refresh", font=('Helvetica', 12),
                          command=lambda: self._loadAccounts(accountsTree))
        refreshBtn.pack(side=LEFT, padx=5)
        
        treeFrame = Frame(frame)
        treeFrame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        columns = ('account_number', 'name', 'balance', 'status', 'date_opened')
        accountsTree = ttk.Treeview(treeFrame, columns=columns, show='headings')
        
        accountsTree.heading('account_number', text='Account Number')
        accountsTree.heading('name', text='Name')
        accountsTree.heading('balance', text='Balance')
        accountsTree.heading('status', text='Status')
        accountsTree.heading('date_opened', text='Date Opened')
        
        accountsTree.column('account_number', width=120)
        accountsTree.column('name', width=180)
        accountsTree.column('balance', width=120)
        accountsTree.column('status', width=100)
        accountsTree.column('date_opened', width=120)
        
        yScrollbar = ttk.Scrollbar(treeFrame, orient=VERTICAL, command=accountsTree.yview)
        accountsTree.configure(yscrollcommand=yScrollbar.set)
        
        accountsTree.pack(side=LEFT, fill=BOTH, expand=True)
        yScrollbar.pack(side=RIGHT, fill=Y)
        
        accountsTree.bind('<Double-1>', lambda e: self._viewAccountDetails(accountsTree))
        
        actionsFrame = Frame(frame)
        actionsFrame.pack(fill=X, padx=20, pady=10)
        
        viewBtn = Button(actionsFrame, text="View Details", font=('Helvetica', 12),
                        command=lambda: self._viewAccountDetails(accountsTree))
        viewBtn.pack(side=LEFT, padx=5)
        
        editBtn = Button(actionsFrame, text="Edit Account", font=('Helvetica', 12),
                        command=lambda: self._editAccount(accountsTree))
        editBtn.pack(side=LEFT, padx=5)
        
        deleteBtn = Button(actionsFrame, text="Delete Account", font=('Helvetica', 12),
                         bg='#ff4444', fg='white',
                         command=lambda: self._deleteAccount(accountsTree))
        deleteBtn.pack(side=LEFT, padx=5)
        
        self._loadAccounts(accountsTree)
    
    def _loadAccounts(self, tree):
        """Load accounts into the treeview"""
        for item in tree.get_children():
            tree.delete(item)
        
        accounts = self.bank.getAllAccounts()
        
        for account in accounts:
            if account.accountNumber.lower() == 'admin':
                continue
                
            name = f"{account.fName} {account.lName}"
            balance = f"PHP {account.balance:.2f}"
            date = account.dateOpened.strftime("%Y-%m-%d")
            
            tree.insert('', 'end', values=(
                account.accountNumber,
                name,
                balance,
                account.status,
                date
            ))

    def _setupTransactionsTab(self, frame):
        """Set up the transactions history tab"""
        header = Label(frame, text="Transaction History", font=('Helvetica', 18, 'bold'))
        header.pack(pady=20)
        
        accountFrame = Frame(frame)
        accountFrame.pack(fill=X, padx=20, pady=10)
        accountLabel = Label(accountFrame, text="Select Account:", font=('Helvetica', 12))
        accountLabel.pack(side=LEFT, padx=5)
        accountEntry = Entry(accountFrame, font=('Helvetica', 12), width=20)
        accountEntry.pack(side=LEFT, padx=5)
        loadBtn = Button(accountFrame, text="Load Transactions", font=('Helvetica', 12),
                       command=lambda: self._loadTransactions(accountEntry.get(), transTree))
        loadBtn.pack(side=LEFT, padx=5)
        
        treeFrame = Frame(frame)
        treeFrame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        columns = ('date', 'description', 'amount', 'transacId')
        transTree = ttk.Treeview(treeFrame, columns=columns, show='headings')
        transTree.heading('date', text='Date')
        transTree.heading('description', text='Description')
        transTree.heading('amount', text='Amount')
        transTree.heading('transacId', text='Transaction ID')
        transTree.column('date', width=150)
        transTree.column('description', width=300)
        transTree.column('amount', width=100)
        transTree.column('transacId', width=100)
        
        yScrollbar = ttk.Scrollbar(treeFrame, orient=VERTICAL, command=transTree.yview)
        transTree.configure(yscrollcommand=yScrollbar.set)
        transTree.pack(side=LEFT, fill=BOTH, expand=True)
        yScrollbar.pack(side=RIGHT, fill=Y)

    def _setupSystemTab(self, frame):
        """Set up the system tab with admin functions and system stats"""
        header = Label(frame, text="System Administration", font=('Helvetica', 18, 'bold'))
        header.pack(pady=20)
        
        contentFrame = Frame(frame)
        contentFrame.pack(fill=BOTH, expand=True, padx=20)
        
        leftFrame = Frame(contentFrame, width=450)
        leftFrame.pack(side=LEFT, fill=Y, padx=10, pady=10)
        
        pwdFrame = LabelFrame(leftFrame, text="Change Admin Password", font=('Helvetica', 12, 'bold'), width=450)
        pwdFrame.pack(fill=X, pady=10)
        
        oldPwdFrame = Frame(pwdFrame)
        oldPwdFrame.pack(fill=X, pady=5)
        
        oldPwdLabel = Label(oldPwdFrame, text="Current Password:", font=('Helvetica', 12))
        oldPwdLabel.pack(side=LEFT, padx=10)
        
        oldPwdEntry = Entry(oldPwdFrame, show="*", font=('Helvetica', 12), width=20)
        oldPwdEntry.pack(side=RIGHT, padx=5)
        
        newPwdFrame = Frame(pwdFrame)
        newPwdFrame.pack(fill=X, pady=5)
        
        newPwdLabel = Label(newPwdFrame, text="New Password:", font=('Helvetica', 12))
        newPwdLabel.pack(side=LEFT, padx=10)
        
        newPwdEntry = Entry(newPwdFrame, show="*", font=('Helvetica', 12), width=20)
        newPwdEntry.pack(side=RIGHT, padx=5)
        
        confirmPwdFrame = Frame(pwdFrame)
        confirmPwdFrame.pack(fill=X, pady=5)
        
        confirmPwdLabel = Label(confirmPwdFrame, text="Confirm Password:", font=('Helvetica', 12))
        confirmPwdLabel.pack(side=LEFT, padx=10)
        
        confirmPwdEntry = Entry(confirmPwdFrame, show="*", font=('Helvetica', 12), width=20)
        confirmPwdEntry.pack(side=RIGHT, padx=5)
        
        changePwdBtn = Button(pwdFrame, text="Change Password", font=('Helvetica', 12),
                             command=lambda: self._changeAdminPassword(
                                 oldPwdEntry.get(),
                                 newPwdEntry.get(),
                                 confirmPwdEntry.get()
                             ))
        changePwdBtn.pack(pady=10)
        
        rightFrame = Frame(contentFrame, width=450)
        rightFrame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
        
        statsFrame = LabelFrame(rightFrame, text="System Statistics", font=('Helvetica', 12, 'bold'))
        statsFrame.pack(fill=BOTH, expand=True, pady=10)
        
        self.statsLabels = {}
        self._createStatsDisplay(statsFrame)
        
        refreshStatsBtn = Button(statsFrame, text="Refresh Statistics", 
                               font=('Helvetica', 12),
                               command=lambda: self._refreshSystemStats())
        refreshStatsBtn.pack(pady=15)
        
        self._refreshSystemStats()

    def _createStatsDisplay(self, frame):
        """Create the system statistics display widgets with detailed account status counts"""
        # Account statistics section
        accountsHeaderFrame = Frame(frame)
        accountsHeaderFrame.pack(fill=X, pady=5, padx=20)
        Label(accountsHeaderFrame, text="Account Statistics", 
            font=('Helvetica', 12, 'bold', 'underline')).pack(anchor=W)
        
        # Total accounts 
        totalAccFrame = Frame(frame)
        totalAccFrame.pack(fill=X, pady=5, padx=20)
        Label(totalAccFrame, text="Total Customer Accounts:", 
            font=('Helvetica', 12, 'bold')).pack(side=LEFT)
        self.statsLabels['total_accounts'] = Label(totalAccFrame, 
                                            text="0", 
                                            font=('Helvetica', 12))
        self.statsLabels['total_accounts'].pack(side=LEFT, padx=10)
        
        # Account status breakdown section - Added detailed status counts
        statusFrame = LabelFrame(frame, text="Account Status Breakdown", font=('Helvetica', 11))
        statusFrame.pack(fill=X, pady=5, padx=20)
        
        # Active accounts
        activeAccFrame = Frame(statusFrame)
        activeAccFrame.pack(fill=X, pady=3)
        Label(activeAccFrame, text="Active:", 
            font=('Helvetica', 11)).pack(side=LEFT, padx=10)
        self.statsLabels['active_accounts'] = Label(activeAccFrame, 
                                            text="0", 
                                            font=('Helvetica', 11),
                                            fg='green')
        self.statsLabels['active_accounts'].pack(side=LEFT, padx=5)
        
        # Inactive accounts
        inactiveAccFrame = Frame(statusFrame)
        inactiveAccFrame.pack(fill=X, pady=3)
        Label(inactiveAccFrame, text="Inactive:", 
            font=('Helvetica', 11)).pack(side=LEFT, padx=10)
        self.statsLabels['inactive_accounts'] = Label(inactiveAccFrame, 
                                                text="0", 
                                                font=('Helvetica', 11),
                                                fg='orange')
        self.statsLabels['inactive_accounts'].pack(side=LEFT, padx=5)
        
        # Suspended accounts
        suspendedAccFrame = Frame(statusFrame)
        suspendedAccFrame.pack(fill=X, pady=3)
        Label(suspendedAccFrame, text="Suspended:", 
            font=('Helvetica', 11)).pack(side=LEFT, padx=10)
        self.statsLabels['suspended_accounts'] = Label(suspendedAccFrame, 
                                                text="0", 
                                                font=('Helvetica', 11),
                                                fg='red')
        self.statsLabels['suspended_accounts'].pack(side=LEFT, padx=5)
        
        # Closed accounts
        closedAccFrame = Frame(statusFrame)
        closedAccFrame.pack(fill=X, pady=3)
        Label(closedAccFrame, text="Closed:", 
            font=('Helvetica', 11)).pack(side=LEFT, padx=10)
        self.statsLabels['closed_accounts'] = Label(closedAccFrame, 
                                            text="0", 
                                            font=('Helvetica', 11),
                                            fg='gray')
        self.statsLabels['closed_accounts'].pack(side=LEFT, padx=5)
        
        # Financial statistics section
        financialHeaderFrame = Frame(frame)
        financialHeaderFrame.pack(fill=X, pady=5, padx=20)
        Label(financialHeaderFrame, text="Financial Statistics", 
            font=('Helvetica', 12, 'bold', 'underline')).pack(anchor=W, pady=(10,0))
        
        balanceFrame = Frame(frame)
        balanceFrame.pack(fill=X, pady=5, padx=20)
        Label(balanceFrame, text="Total Customer Balance:", 
            font=('Helvetica', 12, 'bold')).pack(side=LEFT)
        self.statsLabels['total_balance'] = Label(balanceFrame, 
                                            text="PHP 0.00", 
                                            font=('Helvetica', 12))
        self.statsLabels['total_balance'].pack(side=LEFT, padx=10)
        
        # Transaction statistics section
        transHeaderFrame = Frame(frame)
        transHeaderFrame.pack(fill=X, pady=5, padx=20)
        Label(transHeaderFrame, text="Transaction Statistics", 
            font=('Helvetica', 12, 'bold', 'underline')).pack(anchor=W, pady=(10,0))
        
        recentTransFrame = Frame(frame)
        recentTransFrame.pack(fill=X, pady=5, padx=20)
        Label(recentTransFrame, text="Transactions (Last 7 Days):", 
            font=('Helvetica', 12, 'bold')).pack(side=LEFT)
        self.statsLabels['recent_transactions'] = Label(recentTransFrame, 
                                                text="0", 
                                                font=('Helvetica', 12))
        self.statsLabels['recent_transactions'].pack(side=LEFT, padx=10)
        
        # Last updated timestamp
        updateTimeFrame = Frame(frame)
        updateTimeFrame.pack(fill=X, pady=10, padx=20)
        Label(updateTimeFrame, text="Last Updated:", 
            font=('Helvetica', 10)).pack(side=LEFT)
        self.statsLabels['update_time'] = Label(updateTimeFrame, 
                                        text="Never", 
                                        font=('Helvetica', 10))
        self.statsLabels['update_time'].pack(side=LEFT, padx=10)

    def _refreshSystemStats(self):
        """Refresh the system statistics display with detailed account status counts"""
        try:
            stats = self._getCustomerStats()
            
            self.statsLabels['total_accounts'].config(text=str(stats['total_accounts']))
            self.statsLabels['active_accounts'].config(text=str(stats['active_accounts']))
            self.statsLabels['inactive_accounts'].config(text=str(stats['inactive_accounts']))
            self.statsLabels['suspended_accounts'].config(text=str(stats['suspended_accounts']))
            self.statsLabels['closed_accounts'].config(text=str(stats['closed_accounts']))
            self.statsLabels['total_balance'].config(text=f"PHP {stats['total_balance']:.2f}")
            self.statsLabels['recent_transactions'].config(text=str(stats['recent_transactions']))
            
            currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.statsLabels['update_time'].config(text=currentTime)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load system statistics: {str(e)}")

    def _getCustomerStats(self):
        """Get detailed system statistics with account status breakdown"""
        # Initialize statistics dictionary with default values
        stats = {
            'total_accounts': 0,
            'active_accounts': 0,
            'inactive_accounts': 0, 
            'suspended_accounts': 0,
            'closed_accounts': 0,
            'total_balance': 0.0,
            'recent_transactions': 0
        }
        
        try:
            # Get all accounts from the system
            accounts = self.bank.getAllAccounts()
            
            # Filter out admin accounts
            customer_accounts = [acc for acc in accounts if acc.accountNumber.lower() != 'admin']
            
            # Count total customer accounts
            stats['total_accounts'] = len(customer_accounts)
            
            # Count accounts by status with case-insensitive comparison
            for account in customer_accounts:
                status = account.status.lower()
                
                # Add balance to total
                stats['total_balance'] += account.balance
                
                # Count accounts by status
                if status == 'active':
                    stats['active_accounts'] += 1
                elif status == 'inactive':
                    stats['inactive_accounts'] += 1
                elif status == 'suspended':
                    stats['suspended_accounts'] += 1
                elif status == 'closed':
                    stats['closed_accounts'] += 1
            
            # Get transaction statistics from bank service
            try:
                bank_stats = self.bank.getSystemStats()
                stats['recent_transactions'] = bank_stats.get('recent_transactions', 0)
            except Exception:
                # Handle missing transaction data gracefully
                pass
                
            return stats
            
        except Exception as e:
            print(f"Error calculating customer statistics: {e}")
            # Return default stats in case of error
            return stats

    def _findAccount(self, accountId):
        """Efficient account lookup function"""
        import csv
        from datetime import datetime
        from models.account import Account
        
        targetId = str(accountId).strip()
        
        try:
            account = self.bank.getAccount(accountId)
            if account:
                return account
                
            with open('Tam-Bank/userinfo/accounts.csv', 'r') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    rowId = str(row['Account Number']).strip()                    
                    if (rowId == targetId or 
                        rowId.replace(" ", "") == targetId.replace(" ", "")):
                        account = Account(
                            rowId,
                            row['First Name'],
                            row['Last Name'],
                            float(row['Balance']),
                            row['Mobile Number'],
                            row['Email']
                        )
                        
                        account.status = row['Status']
                        try:
                            account.dateOpened = datetime.strptime(row['Date Opened'], '%Y-%m-%d %H:%M:%S')
                        except (ValueError, KeyError):
                            account.dateOpened = datetime.now()
                        
                        if 'Password Hash' in row:
                            account.passHash = row['Password Hash']
                        
                        return account
            
            return None
            
        except Exception as e:
            return None

    def _viewAccountDetails(self, tree):
        """View details of selected account"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an account to view")
            return
            
        accountId = tree.item(selected[0])['values'][0]
        account = self._findAccount(accountId)
        
        if not account:
            messagebox.showerror("Error", f"Account {accountId} not found")
            return
        
        detailWindow = Toplevel(self.mainWindow)
        detailWindow.title(f"Account Details - {accountId}")
        detailWindow.geometry("500x400")
        detailWindow.grab_set()
        
        Label(detailWindow, text=f"Account Details", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        detailsFrame = Frame(detailWindow)
        detailsFrame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        fields = [
            ("Account Number", account.accountNumber),
            ("Full Name", f"{account.fName} {account.lName}"),
            ("Balance", f"PHP {account.balance:.2f}"),
            ("Mobile", account.mobileNo),
            ("Email", account.email),
            ("Status", account.status),
            ("Date Opened", account.dateOpened.strftime("%Y-%m-%d %H:%M:%S"))
        ]
        
        for i, (field, value) in enumerate(fields):
            Label(detailsFrame, text=field, font=('Helvetica', 12, 'bold')).grid(row=i, column=0, sticky=W, pady=5)
            Label(detailsFrame, text=value, font=('Helvetica', 12)).grid(row=i, column=1, sticky=W, pady=5)
        
        btnFrame = Frame(detailWindow)
        btnFrame.pack(fill=X, pady=10)
        
        editBtn = Button(btnFrame, text="Edit Account", font=('Helvetica', 12),
                    command=lambda: self._editAccountFromDetails(account, detailWindow))
        editBtn.pack(side=LEFT, padx=10)
        
        closeBtn = Button(btnFrame, text="Close", font=('Helvetica', 12),
                        command=detailWindow.destroy)
        closeBtn.pack(side=RIGHT, padx=10)

    def _editAccount(self, tree):
        """Edit selected account"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an account to edit")
            return
            
        accountId = tree.item(selected[0])['values'][0]
        account = self._findAccount(accountId)
        
        if not account:
            messagebox.showerror("Error", f"Account {accountId} not found")
            return
            
        self._showEditForm(account)
    
    def _editAccountFromDetails(self, account, detailWindow):
        """Edit account from details window"""
        detailWindow.destroy()
        self._showEditForm(account)
    
    def _showEditForm(self, account):
        """Show form to edit account"""
        editWindow = Toplevel(self.mainWindow)
        editWindow.title(f"Edit Account - {account.accountNumber}")
        editWindow.geometry("500x500")
        editWindow.grab_set()
        
        Label(editWindow, text=f"Edit Account", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        formFrame = Frame(editWindow)
        formFrame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        idFrame = Frame(formFrame)
        idFrame.pack(fill=X, pady=5)
        Label(idFrame, text="Account ID:", width=15, anchor=W).pack(side=LEFT)
        idVar = StringVar(value=account.accountNumber)
        idEntry = Entry(idFrame, textvariable=idVar, font=('Helvetica', 12))
        idEntry.pack(side=LEFT, fill=X, expand=True)
        
        fnameFrame = Frame(formFrame)
        fnameFrame.pack(fill=X, pady=5)
        Label(fnameFrame, text="First Name:", width=15, anchor=W).pack(side=LEFT)
        fnameVar = StringVar(value=account.fName)
        fnameEntry = Entry(fnameFrame, textvariable=fnameVar, font=('Helvetica', 12))
        fnameEntry.pack(side=LEFT, fill=X, expand=True)
        
        lnameFrame = Frame(formFrame)
        lnameFrame.pack(fill=X, pady=5)
        Label(lnameFrame, text="Last Name:", width=15, anchor=W).pack(side=LEFT)
        lnameVar = StringVar(value=account.lName)
        lnameEntry = Entry(lnameFrame, textvariable=lnameVar, font=('Helvetica', 12))
        lnameEntry.pack(side=LEFT, fill=X, expand=True)
        
        mobileFrame = Frame(formFrame)
        mobileFrame.pack(fill=X, pady=5)
        Label(mobileFrame, text="Mobile:", width=15, anchor=W).pack(side=LEFT)
        mobileVar = StringVar(value=account.mobileNo)
        mobileEntry = Entry(mobileFrame, textvariable=mobileVar, font=('Helvetica', 12))
        mobileEntry.pack(side=LEFT, fill=X, expand=True)
        
        emailFrame = Frame(formFrame)
        emailFrame.pack(fill=X, pady=5)
        Label(emailFrame, text="Email:", width=15, anchor=W).pack(side=LEFT)
        emailVar = StringVar(value=account.email)
        emailEntry = Entry(emailFrame, textvariable=emailVar, font=('Helvetica', 12))
        emailEntry.pack(side=LEFT, fill=X, expand=True)
        
        statusFrame = Frame(formFrame)
        statusFrame.pack(fill=X, pady=5)
        Label(statusFrame, text="Status:", width=15, anchor=W).pack(side=LEFT)
        statusVar = StringVar(value=account.status)
        statusCombo = ttk.Combobox(statusFrame, textvariable=statusVar,state='readonly', 
                                  values=["Active", "Inactive", "Suspended", "Closed"])
        statusCombo.pack(side=LEFT, fill=X, expand=True)
        
        passwordFrame = Frame(formFrame)
        passwordFrame.pack(fill=X, pady=5)
        Label(passwordFrame, text="New Password:", width=15, anchor=W).pack(side=LEFT)
        passwordVar = StringVar()
        passwordEntry = Entry(passwordFrame, textvariable=passwordVar, font=('Helvetica', 12), show="*")
        passwordEntry.pack(side=LEFT, fill=X, expand=True)
        
        btnFrame = Frame(editWindow)
        btnFrame.pack(fill=X, pady=10)
        
        saveBtn = Button(btnFrame, text="Save Changes", font=('Helvetica', 12),
                       command=lambda: self._saveAccountChanges(
                           account.accountNumber,
                           idVar.get(),
                           fnameVar.get(),
                           lnameVar.get(),
                           mobileVar.get(),
                           emailVar.get(),
                           statusVar.get(),
                           passwordVar.get(),
                           editWindow
                       ))
        saveBtn.pack(side=LEFT, padx=10)
        
        cancelBtn = Button(btnFrame, text="Cancel", font=('Helvetica', 12),
                        command=editWindow.destroy)
        cancelBtn.pack(side=RIGHT, padx=10)
    
    def _saveAccountChanges(self, originalId, newId, fname, lname, mobile, email, status, password, window):
        """Save changes to account"""
        try:
            if not newId.isdigit():
                messagebox.showerror("Error", "Account ID must be numeric")
                return
            
            accountId = int(newId)
            if not (20210000 <= accountId <= 20230000):
                messagebox.showerror("Error", "Account ID must be in the range 20210000 - 20230000")
                return
            
            if not fname.isalpha() or not lname.isalpha():
                messagebox.showerror("Error", "First and last names must contain only letters")
                return
            
            if not (mobile.isdigit() and mobile.startswith('09') and len(mobile) == 11):
                messagebox.showerror('Error', 'Invalid phone number. It should start with 09 and have 11 digits.')
                return
            
            if '@' not in email or '.' not in email:
                messagebox.showerror('Error', 'Invalid email address.')
                return
            
            if newId != originalId and newId in [acc.accountNumber for acc in self.bank.getAllAccounts() if acc.accountNumber != originalId]:
                messagebox.showerror('Error', f'Account ID {newId} already exists. Please choose another ID.')
                return

            success = self.bank.adminUpdateAccount(
                originalId, newId, fname, lname, mobile, email, status, password
            )
            
            if success:
                messagebox.showinfo("Success", "Account updated successfully")
                window.destroy()
                
                for tab in self.mainWindow.winfo_children():
                    if isinstance(tab, ttk.Notebook):
                        for tabId in tab.tabs():
                            tabName = tab.tab(tabId, "text")
                            if tabName == "Account Management":
                                tabFrame = self.mainWindow.nametowidget(tabId)
                                for widget in tabFrame.winfo_children():
                                    if isinstance(widget, Frame):
                                        for child in widget.winfo_children():
                                            if isinstance(child, ttk.Treeview):
                                                self._loadAccounts(child)
                                                break
                
                if hasattr(self, 'statsLabels'):
                    self._refreshSystemStats()
            else:
                messagebox.showerror("Error", "Failed to update account")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating account: {str(e)}")
    
    def _deleteAccount(self, tree):
        """Delete selected account"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an account to delete")
            return
            
        accountId = tree.item(selected[0])['values'][0]
        
        confirm = messagebox.askyesno("Confirm Deletion", 
                                   f"Are you sure you want to permanently delete account {accountId}?\n\n"
                                   "This action cannot be undone.")
        
        if confirm:
            try:
                success = self.bank.adminDeleteAccount(accountId)
                
                if success:
                    messagebox.showinfo("Success", f"Account {accountId} deleted successfully")
                    self._loadAccounts(tree)
                    
                    if hasattr(self, 'statsLabels'):
                        self._refreshSystemStats()
                else:
                    messagebox.showerror("Error", "Failed to delete account")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting account: {str(e)}")
    
    def _loadTransactions(self, accountId, tree):
        """Load transactions for specified account"""
        if not accountId:
            messagebox.showwarning("No Account", "Please enter an account number")
            return
            
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            transactions = self.bank.getAccountTransactions(accountId)
            
            if not transactions:
                tree.insert('', 'end', values=('', 'No transactions found', '', ''))
            else:
                for transaction in transactions:
                    try:
                        if hasattr(transaction['date'], 'strftime'):
                            dateStr = transaction['date'].strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            dateStr = str(transaction['date'])
                        
                        if float(transaction['amount']) >= 0:
                            amountStr = f"PHP +{float(transaction['amount']):.2f}"
                            tag = 'positive'
                        else:
                            amountStr = f"PHP {float(transaction['amount']):.2f}"
                            tag = 'negative'
                        
                        transacId = transaction.get('transacId', 
                                             transaction.get('transaction_id', ''))
                        description = transaction.get('description', 'Transaction')
                        
                        itemId = tree.insert('', 'end', values=(
                            dateStr, description, amountStr, transacId
                        ))
                        
                        if tag == 'positive':
                            tree.tag_configure('positive', foreground='green')
                            tree.item(itemId, tags=('positive',))
                        elif tag == 'negative':
                            tree.tag_configure('negative', foreground='red')
                            tree.item(itemId, tags=('negative',))
                            
                    except (KeyError, ValueError, AttributeError):
                        continue
        except Exception as e:
            messagebox.showerror("Error", f"Could not load transactions: {str(e)}")
    
    def _searchAccounts(self, searchTerm, tree):
        """Search for accounts matching the search term"""
        if not searchTerm:
            self._loadAccounts(tree)
            return
            
        for item in tree.get_children():
            tree.delete(item)
        
        accounts = self.bank.getAllAccounts()
        
        searchTerm = searchTerm.lower()
        filteredAccounts = []
        
        for account in accounts:
            if account.accountNumber.lower() == 'admin':
                continue
                
            if (searchTerm in account.accountNumber.lower() or
                searchTerm in account.fName.lower() or
                searchTerm in account.lName.lower()):
                filteredAccounts.append(account)
        
        for account in filteredAccounts:
            name = f"{account.fName} {account.lName}"
            balance = f"PHP {account.balance:.2f}"
            date = account.dateOpened.strftime("%Y-%m-%d")
            
            tree.insert('', 'end', values=(
                account.accountNumber,
                name,
                balance,
                account.status,
                date
            ))
    
    def _changeAdminPassword(self, oldPassword, newPassword, confirmPassword):
        """Change admin password with comprehensive debugging"""
        if not oldPassword or not newPassword or not confirmPassword:
            messagebox.showerror("Error", "All fields are required")
            return
            
        if newPassword != confirmPassword:
            messagebox.showerror("Error", "New passwords do not match")
            return
        
        hasDigit = any(char.isdigit() for char in newPassword)
        hasLetter = any(char.isalpha() for char in newPassword)
        hasSpecial = any(not char.isalnum() for char in newPassword)

        if len(newPassword) < 8 or not (hasDigit and hasLetter and hasSpecial):
            messagebox.showerror("Error", "Password must be at least 8 characters long and contain at least one digit, one letter, and one special character")
            return
        
        try:
            success = self.bank.updateAdminPassword(oldPassword, newPassword)
            
            if success:
                messagebox.showinfo("Success", f"Admin password changed successfully to: {newPassword}\n\nPlease remember this password for your next login.")
            else:
                messagebox.showerror("Error", "Failed to change password. The current password may be incorrect.")
        except Exception as e:
            messagebox.showerror("Error", f"Error changing password: {str(e)}")
    
    def _logout(self):
        """Log out and return to login screen"""
        self.mainWindow.destroy()
        
        from interface.interface import GUIinterface
        gui = GUIinterface(self.bank)
        gui.start()