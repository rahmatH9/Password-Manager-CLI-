# Password-Manager-CLI-

A Python-based Command Line Password Manager with AES-encrypted storage, master password protection, logging, and backup functionality.

Features AES-256 Encryption using Fernet (with PBKDF2 Key Derivation and Salt) Master Password Protection with 3 Attempt Lockout Add, View, Search, Update, and Delete Passwords securely Auto-generate Strong Passwords on demand Activity Logging to logs.txt for operation tracking Data Export & Import for safe backups and restores CLI-based Interface with simple navigation Built with Python 3, Cryptography, and Colorama

Requirements Python 3.x Cryptography

pip install cryptography colorama

Usage Example

Run the password manager
python password_manager.py

On first run, you'll be asked to set a Master Password Access your stored credentials securely after verifying with the Master Password Perform Add, View, Search, Update, Delete, Export, and Import actions from the CLI menu

How it Works

Key Derivation: Uses PBKDF2 with SHA-256 and a random salt to derive a secure key from your Master Password. Encryption: Password entries are encrypted with Fernet symmetric encryption before storage. Master Password Protection: Without the correct master key, password data remains inaccessible. Logging: Every critical operation is logged with timestamps for accountability. Backup & Import: Allows exporting data for backup and importing from a backup securely.

Disclaimer

This tool is for personal and ethical use only. If you forget your Master Password, your stored data will be irrecoverable. Always ensure your data files are stored securely to prevent unauthorized access.

