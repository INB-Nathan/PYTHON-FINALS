# 🏦 TAMBANK - Banking System

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/Status-Development-yellow.svg" alt="Status: Development"/>
</div>

<div align="center">
  <p><strong>A comprehensive banking system built in Python</strong></p>
  <p>2TSY2425_IT0011_TC22-9 - Pykings</p>
</div>

## 📋 Project Description

TamBank is a secure and user-friendly banking system developed in Python. It offers a complete suite of account management and transaction processing capabilities, featuring secure password authentication, transaction recording, and persistent data storage.

The system provides command-line interface for managing bank accounts, performing financial transactions, and maintaining account security. It simulates core banking functionalities with proper error handling and data validation.

## ✨ Features

### 🔒 Account Management
- **User Authentication** - Secure login with SHA-256 password hashing
- **Account Creation** - Register new accounts with initial deposits
- **Account Details** - View comprehensive account information
- **Profile Updates** - Modify personal information
- **Account Closure** - Close accounts with proper fund handling

### 💰 Transaction Processing
- **Deposits** - Add funds to accounts with transaction recording
- **Withdrawals** - Remove funds with balance verification
- **Transaction History** - View detailed transaction logs
- **Balance Inquiries** - Check current account balance

### 🛡️ Security Features
- **Password Encryption** - Secure password storage using SHA-256 with salt
- **Session Management** - Proper user authentication and session handling
- **Data Validation** - Input validation to prevent invalid transactions
- **Error Handling** - Comprehensive error handling for all operations

### 📊 Data Management
- **CSV Storage** - Persistent data storage for accounts and transactions
- **Transaction Logging** - Detailed recording of all financial activities

## 🔧 Libraries Used

- **Python 3.8+** - Core programming language
- **hashlib** - Password encryption
- **datetime** - Transaction and account timestamp handling
- **csv** - Data storage and management

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Basic understanding of command-line interfaces

### Installation

1. Clone the repository
```bash
git clone https://github.com/INB-Nathan/PYTHON-FINALS.git
cd PYTHON-FINALS/Tam-Bank
```

2. Ensure directory structure
```
Tam-Bank/
├── main.py
├── userinfo/
│   ├── accounts.csv
│   └── transactions.csv
```

3. Run the application
```bash
python main.py
```

## 📱 Usage Examples

### Creating an Account
```
===== REGISTER =====
First Name: John
Last Name: Doe
Initial Balance: 1000
Mobile Number: 09123456789
Email: john.doe@example.com
Password: ********
Confirm Password: ********

Account created successfully!
Your Account Number is: 20210123
Please save this number for future login.
```

### Depositing Funds
```
===== DEPOSIT =====
Enter amount to deposit: PHP500
Deposited PHP500.00. New balance: PHP1500.00
```

### Viewing Transaction History
```
===== TRANSACTION HISTORY =====
DATE                 DESCRIPTION         AMOUNT      BALANCE    
--------------------------------------------------------------------
2025-03-15 09:15     Initial Deposit     PHP1000.00  PHP1000.00 
2025-03-15 09:20     Deposit             PHP500.00   PHP1500.00 
```

## 👥 Team Members

| Member | GitHub Username | Name |
|--------|----------------|------|
| <img src="https://github.com/orljorstin.png" width="30" height="30" alt="@orljorstin"/> | [@orljorstin](https://github.com/orljorstin) | Camama, Earl Justin |
| <img src="https://github.com/Dane-000.png" width="30" height="30" alt="@Dane-000"/> | [@Dane-000](https://github.com/Dane-000) | Borja, Fernando Dane |
| <img src="https://github.com/INB-Nathan.png" width="30" height="30" alt="@INB-Nathan"/> | [@INB-Nathan](https://github.com/INB-Nathan) | Cabrales, Nathan Josua |
| <img src="https://github.com/G10dero.png" width="30" height="30" alt="@G10dero"/> | [@G10dero](https://github.com/G10dero) | Tendero, Guinevere |


## 📊 Project Status

Last Updated: 2025-03-15
Status: Under Development

---

<div align="center">
  <p>© 2025 Pykings Team. All Rights Reserved.</p>
</div>
