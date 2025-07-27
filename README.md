# Password-Manager-CLI-
📌 Project Overview

This Command-Line Password Manager is a secure, offline solution that allows users to manage credentials with AES-256 encryption using the Fernet module from Python’s cryptography library. The manager provides a menu-driven interface for operations like add, view, search, update, delete, import, export, and auto-generate passwords with full master password protection.

✅ Key Features

| Feature                        | Description                                                    |
| ------------------------------ | -------------------------------------------------------------- |
| AES-256 Encryption             | Uses `Fernet` to encrypt/decrypt passwords securely            |
| Master Password Authentication | bcrypt-hashed master password for login with 3-attempt lockout |
| Clipboard Cleaning             | Securely clears clipboard after copy (optional)                |
| Auto Password Generator        | Strong random password generator                               |
| Secure Import/Export           | Encrypted JSON backup and restore                              |
| Activity Logging               | Timestamped logs for actions (stored in `logs.txt`)            |
| Session Timeout (optional)     | Auto logout after inactivity (future scope)                    |


⚙️ Technology Stack

Language: Python 3.x

Libraries: cryptography, bcrypt, colorama, json, getpass, os, pyperclip, time, datetime

Data Storage: JSON File (encrypted)

Platform: Linux/MacOS/Windows CLI

🧩 Project Components

1. password_manager.py
Main script and CLI interface

2. data/credentials.json.enc
Encrypted password storage file

3. master.key
Stores bcrypt-hashed master password

4. logs.txt
Stores timestamped logs of critical operations

🛠️ Functional Architecture Diagram

+----------------------+
|    User Interface    |
|  (Command Line CLI)  |
+----------+-----------+
           |
           v
+----------------------+
|   Master Auth Layer  |<-- bcrypt verification (3-attempt lockout)
+----------+-----------+
           |
           v
+-------------------------------+
| AES-256 Encryption Module     |<-- Fernet (Encrypt/Decrypt)
+-------------------------------+
           |
           v
+----------------------------+
| JSON Storage / Export /   |
| Import / Logging           |
+----------------------------+


🔄 Process Flow

📌 First Run:
Set master password → hashed with bcrypt → stored in master.key.

📌 Normal Use:
Prompt for master password → check bcrypt hash.

On success → decrypt JSON file with Fernet.

Show CLI Menu:

[1] Add new password

[2] View all

[3] Search entry

[4] Update password

[5] Delete entry

[6] Export (Encrypted)

[7] Import (Encrypted)

[8] Generate password

[9] Quit

Log action in logs.txt

🔑 Key Functionalities

🔐 Master Password Authentication

from getpass import getpass
import bcrypt

def verify_master_password():
    master_password = getpass("Enter master password: ")
    with open("master.key", "rb") as f:
        hashed = f.read()
    return bcrypt.checkpw(master_password.encode(), hashed)

🔒 AES-256 Encryption / Decryption (Fernet)

from cryptography.fernet import Fernet

def load_key():
    return open("secret.key", "rb").read()

def encrypt_data(data):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(data):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(data).decode()

🔍 Search & Display Entry

def search_entry(site):
    with open("credentials.json", "r") as f:
        creds = json.load(f)
    return creds.get(site)

🔄 Import / Export (Encrypted JSON)

def export_data():
    with open("credentials.json", "r") as f:
        data = f.read()
    encrypted = encrypt_data(data)
    with open("backup.enc", "wb") as f:
        f.write(encrypted)

def import_data():
    with open("backup.enc", "rb") as f:
        encrypted = f.read()
    data = decrypt_data(encrypted)
    with open("credentials.json", "w") as f:
        f.write(data)

🔍 Sample CLI Menu (Display)

========= PASSWORD MANAGER =========
1. Add Password
2. View Passwords
3. Search Password
4. Update Password
5. Delete Password
6. Export (Encrypted)
7. Import (Encrypted)
8. Generate Strong Password
9. Exit
====================================

🛡️ Security Measures

| Measure                  | Explanation                                                             |
| ------------------------ | ----------------------------------------------------------------------- |
| AES-256 (Fernet)         | Ensures stored passwords are encrypted and tamper-proof                 |
| bcrypt-hashed master key | Protects master password with salting and slow hashing                  |
| 3-attempt lockout        | Prevents brute-force login attempts                                     |
| Activity Logs            | Each action is timestamped and saved in `logs.txt`                      |
| Clipboard cleaner        | Prevents password leakage from system clipboard (optional/future scope) |


📁 Folder Structure

password_manager/
│
├── password_manager.py
├── master.key
├── secret.key
├── logs.txt
├── data/
│   ├── credentials.json.enc
│   └── backup.enc


📚 Summary
This Password Manager provides a balance of security, usability, and portability. Built using Python, it demonstrates key principles in data protection, cryptographic design, and secure application development.


Disclaimer

- Personal and Ethical Use: This tool is for personal and ethical use only.
- Master Password Recovery: If you forget your master password, your stored data will be irrecoverable.
- Secure Data Storage: Always ensure your data files are stored securely to prevent unauthorized access.




