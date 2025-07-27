import os
import json
import base64
import getpass
from datetime import datetime
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from colorama import Fore, init
import random
import string
import shutil

init(autoreset=True)

DATA_FILE = 'data.json'
MASTER_FILE = 'master.json'
LOG_FILE = 'logs.txt'


def log_activity(action):
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{datetime.now()}] {action}\n")


def derive_key(password, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100_000)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def load_master():
    if os.path.exists(MASTER_FILE):
        with open(MASTER_FILE, 'r') as f:
            return json.load(f)
    return None


def save_master(master_hash, salt):
    with open(MASTER_FILE, 'w') as f:
        json.dump({"hash": master_hash, "salt": base64.b64encode(salt).decode()}, f)


def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()


def decrypt_data(token, key):
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()


def setup_master():
    print(Fore.YELLOW + "\n🔒 Set Master Password (First Time):")
    password = getpass.getpass("Master Password: ")
    salt = os.urandom(16)
    key = derive_key(password, salt)
    save_master(key.decode(), salt)
    print(Fore.GREEN + "✅ Master password set successfully!")


def verify_master():
    master = load_master()
    if not master:
        setup_master()
        return verify_master()

    for attempt in range(3):
        password = getpass.getpass(Fore.YELLOW + "\n🔑 Enter Master Password: ")
        key = derive_key(password, base64.b64decode(master['salt']))
        if key.decode() == master['hash']:
            print(Fore.GREEN + "✅ Access Granted\n")
            return key
        else:
            print(Fore.RED + "❌ Wrong Password")
    print(Fore.RED + "❌ Too many failed attempts. Exiting.")
    exit()


def load_data():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"accounts": []}


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def add_password(key):
    site = input("Site Name: ")
    username = input("Username: ")
    password = getpass.getpass("Password (Leave blank to auto-generate): ")
    if not password:
        password = generate_strong_password()
        print(Fore.GREEN + f"Generated Password: {password}")
    encrypted_pwd = encrypt_data(password, key)

    data = load_data()
    data['accounts'].append({"site": site, "username": username, "password": encrypted_pwd})
    save_data(data)
    log_activity(f"Added password for {site}")
    print(Fore.GREEN + "✅ Password saved successfully!")


def view_passwords(key):
    data = load_data()
    if not data['accounts']:
        print(Fore.YELLOW + "⚠️ No saved accounts.")
        return
    for idx, acc in enumerate(data['accounts'], 1):
        decrypted_pwd = decrypt_data(acc['password'], key)
        print(Fore.CYAN + f"{idx}. Site: {acc['site']} | Username: {acc['username']} | Password: {decrypted_pwd}")


def search_password(key):
    site_name = input("Enter site name to search: ")
    data = load_data()
    found = False
    for idx, acc in enumerate(data['accounts'], 1):
        if site_name.lower() in acc['site'].lower():
            decrypted_pwd = decrypt_data(acc['password'], key)
            print(Fore.CYAN + f"{idx}. Site: {acc['site']} | Username: {acc['username']} | Password: {decrypted_pwd}")
            found = True
    if not found:
        print(Fore.YELLOW + "❌ No matching entries found.")


def update_password(key):
    data = load_data()
    if not data['accounts']:
        print(Fore.YELLOW + "⚠️ No saved accounts.")
        return
    for idx, acc in enumerate(data['accounts'], 1):
        print(f"{idx}. Site: {acc['site']} | Username: {acc['username']}")
    try:
        idx = int(input("Enter the number to update: ")) - 1
        if 0 <= idx < len(data['accounts']):
            new_password = getpass.getpass("New Password (Leave blank to auto-generate): ")
            if not new_password:
                new_password = generate_strong_password()
                print(Fore.GREEN + f"Generated Password: {new_password}")
            data['accounts'][idx]['password'] = encrypt_data(new_password, key)
            save_data(data)
            log_activity(f"Updated password for {data['accounts'][idx]['site']}")
            print(Fore.GREEN + "✅ Password updated successfully.")
        else:
            print(Fore.RED + "❌ Invalid selection.")
    except ValueError:
        print(Fore.RED + "❌ Invalid input.")


def delete_password():
    data = load_data()
    if not data['accounts']:
        print(Fore.YELLOW + "⚠️ No saved accounts.")
        return
    for idx, acc in enumerate(data['accounts'], 1):
        print(f"{idx}. Site: {acc['site']} | Username: {acc['username']}")
    try:
        idx = int(input("Enter the number to delete: ")) - 1
        if 0 <= idx < len(data['accounts']):
            confirm = input(f"Confirm delete '{data['accounts'][idx]['site']}'? (yes/no): ")
            if confirm.lower() == 'yes':
                deleted = data['accounts'].pop(idx)
                save_data(data)
                log_activity(f"Deleted password for {deleted['site']}")
                print(Fore.GREEN + f"✅ Deleted {deleted['site']}")
            else:
                print(Fore.YELLOW + "❗ Deletion cancelled.")
        else:
            print(Fore.RED + "❌ Invalid selection.")
    except ValueError:
        print(Fore.RED + "❌ Invalid input.")


def change_master_password():
    setup_master()
    log_activity("Changed master password")
    print(Fore.GREEN + "✅ Master Password Changed.")


def export_data():
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy(DATA_FILE, backup_name)
    print(Fore.GREEN + f"✅ Data exported to {backup_name}")
    log_activity(f"Exported data to {backup_name}")


def import_data():
    import_file = input("Enter backup file name to import: ")
    if os.path.exists(import_file):
        shutil.copy(import_file, DATA_FILE)
        print(Fore.GREEN + "✅ Data imported successfully.")
        log_activity(f"Imported data from {import_file}")
    else:
        print(Fore.RED + "❌ File not found.")


def generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


def main():
    key = verify_master()

    while True:
        print(Fore.MAGENTA + """
======== Password Manager Pro ========
1. Add Password
2. View Passwords
3. Search by Site
4. Update Password
5. Delete Password
6. Change Master Password
7. Export Data
8. Import Data
9. Exit
""")
        choice = input("Select an option: ")

        if choice == '1':
            add_password(key)
        elif choice == '2':
            view_passwords(key)
        elif choice == '3':
            search_password(key)
        elif choice == '4':
            update_password(key)
        elif choice == '5':
            delete_password()
        elif choice == '6':
            change_master_password()
            key = verify_master()
        elif choice == '7':
            export_data()
        elif choice == '8':
            import_data()
        elif choice == '9':
            print(Fore.GREEN + "👋 Exiting Password Manager Pro.")
            break
        else:
            print(Fore.RED + "❌ Invalid option. Please try again.")


if __name__ == "__main__":
    main()
