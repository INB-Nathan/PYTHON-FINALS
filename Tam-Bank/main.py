from models.account import Account
from services.bank import TamBank
from interface.interface import GUIinterface
from interface.aInterface import AdminGUIinterface

def main():
    """Main entry point for TamBank application."""
    bank = TamBank()

    app = AdminGUIinterface(bank)
    app.start()
        
if __name__ == "__main__":
    main()