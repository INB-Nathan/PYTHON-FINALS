from services.bank import TamBank
from interface.interface import GUIinterface

def main():
    """Main entry point for TamBank application."""
    bank = TamBank()

    app = GUIinterface(bank)
    app.start()
        
if __name__ == "__main__":
    main()