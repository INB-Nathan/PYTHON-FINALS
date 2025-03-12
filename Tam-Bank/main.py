class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        account_number = input("Enter new account number: ")
        if account_number in self.accounts:
            print("Account already exists.")
        else:
            account_holder = input("Enter account holder's name: ")
            try:
                initial_deposit = float(input("Enter initial deposit amount: "))
                if initial_deposit < 0:
                    print("Initial deposit cannot be negative.")
                    return
                self.accounts[account_number] = {
                    'holder': account_holder,
                    'balance': initial_deposit,
                    'transactions': []
                }
                print("Account created successfully.")
            except ValueError:
                print("Invalid deposit amount. Please enter a number.")

    def view_details(self):
        account_number = input("Enter account number: ")
        if account_number in self.accounts:
            account = self.accounts[account_number]
            print(f"Account Number: {account_number}")
            print(f"Account Holder: {account['holder']}")
            print(f"Balance: {account['balance']}")
        else:
            print("Account not found.")

    def update_account(self):
        account_number = input("Enter account number: ")
        if account_number in self.accounts:
            new_holder_name = input("Enter new account holder's name: ")
            self.accounts[account_number]['holder'] = new_holder_name
            print("Account updated successfully.")
        else:
            print("Account not found.")

    def close_account(self):
        account_number = input("Enter account number: ")
        if account_number in self.accounts:
            del self.accounts[account_number]
            print("Account closed successfully.")
        else:
            print("Account not found.")

    def account_management_menu(self):
        while True:
            print("\n--- Account Management Menu ---")
            print("1. Create an Account")
            print("2. View Details")
            print("3. Update Account")
            print("4. Close Account")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.view_details()
            elif choice == "3":
                self.update_account()
            elif choice == "4":
                self.close_account()
            elif choice == "5":
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
            input("Press Enter to continue...")   
            
bank_system = BankSystem()
bank_system.account_management_menu()
