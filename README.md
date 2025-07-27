# Password-Manager-CLI-
This is a Python-based command line password manager that securely stores and manages passwords using AES-256 encryption. The tool provides a simple and intuitive interface for users to add, view, search, update, and delete passwords.

Features

- AES-256 Encryption: Password entries are encrypted with Fernet symmetric encryption before storage.
- Master Password Protection: The tool requires a master password to access stored credentials, with a 3-attempt lockout feature.
- Add, View, Search, Update, and Delete Passwords: Users can perform various actions on stored passwords.
- Auto-generate Strong Passwords: The tool can generate strong passwords on demand.
- Activity Logging: Every critical operation is logged with timestamps for accountability.
- Data Export & Import: Users can export data for backup and import from a backup securely.

Requirements

- Python 3.x: The tool is built with Python 3 and requires a compatible version.
- Cryptography: The tool uses the cryptography library for encryption and decryption.
- Colorama: The tool uses Colorama for colored output in the command line interface.

Usage

1. Run the password manager using python password_manager.py.
2. On the first run, you'll be asked to set a master password.
3. Access your stored credentials securely after verifying with the master password.
4. Perform various actions like add, view, search, update, delete, export, and import from the CLI menu.

How it Works

1. Key Derivation: The tool uses PBKDF2 with SHA-256 and a random salt to derive a secure key from the master password.
2. Encryption: Password entries are encrypted with Fernet symmetric encryption before storage.
3. Master Password Protection: Without the correct master key, password data remains inaccessible.
4. Logging: Every critical operation is logged with timestamps for accountability.

Security Measures

- AES-256 Encryption: The tool uses AES-256 encryption to secure password entries.
- Master Password Protection: The tool requires a master password to access stored credentials.
- 3-Attempt Lockout: The tool locks out users after 3 incorrect master password attempts.

Backup and Import

- Data Export: Users can export data for backup securely.
- Data Import: Users can import data from a backup securely.

Logging

- Activity Logging: Every critical operation is logged with timestamps for accountability.
- Log File: Logs are stored in a file named logs.txt.

Disclaimer

- Personal and Ethical Use: This tool is for personal and ethical use only.
- Master Password Recovery: If you forget your master password, your stored data will be irrecoverable.
- Secure Data Storage: Always ensure your data files are stored securely to prevent unauthorized access.




