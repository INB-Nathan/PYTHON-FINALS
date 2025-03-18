from models.account import Account
from services.bank import TamBank
from interface.interface import GUIInterface

def main():
    """Main entry point for TamBank application."""
    # Initialize bank service
    bank = TamBank()
    
    # Choose interface (CLI or GUI)
    use_gui = True
    
    if use_gui:
        # Start GUI interface
        app = GUIInterface(bank)
        app.start()
        
if __name__ == "__main__":
    main()