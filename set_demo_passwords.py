import json
from pathlib import Path
from getpass import getpass
from flask_bcrypt import Bcrypt
from flask import Flask

BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = BASE_DIR / "sample_users.json"

app = Flask(__name__)
bcrypt = Bcrypt(app)

with open(USERS_FILE, encoding="utf-8") as file:
    users = json.load(file)

print("Set temporary passwords for your demo accounts.")
print("Use demo-only passwords, not personal passwords.\n")

with app.app_context():
    for user in users:
        username = user["username"]
        password = getpass(f"New password for {username}: ")
        confirm = getpass("Confirm password: ")

        if len(password) < 8:
            print("Password must be at least 8 characters. Run the script again.")
            raise SystemExit(1)

        if password != confirm:
            print("Passwords do not match. Run the script again.")
            raise SystemExit(1)

        user["password_hash"] = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

with open(USERS_FILE, "w", encoding="utf-8") as file:
    json.dump(users, file, indent=2)
    file.write("\n")

print("\nDemo password hashes updated successfully.")
