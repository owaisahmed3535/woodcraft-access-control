import bcrypt
import json
import secrets

users = [
    {
        "id": 1,
        "username": "admin_demo",
        "email": "admin@example.com",
        "role": "admin"
    },
    {
        "id": 2,
        "username": "inventory_demo",
        "email": "inventory@example.com",
        "role": "inventory_manager"
    },
    {
        "id": 3,
        "username": "staff_demo",
        "email": "staff@example.com",
        "role": "staff"
    },
    {
        "id": 4,
        "username": "customer_demo",
        "email": "customer@example.com",
        "role": "customer"
    }
]

for user in users:
    temporary_password = secrets.token_urlsafe(16)
    password_bytes = temporary_password.encode("utf-8")
    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(rounds=12)
    )
    user["password_hash"] = hashed_password.decode("utf-8")

with open("sample_users.json", "w", encoding="utf-8") as file:
    json.dump(users, file, indent=2)

print(f"Created {len(users)} fictional users with bcrypt password hashes.")
print("Only password hashes were saved; temporary passwords were not stored.")
