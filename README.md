# WoodCraft Access Portal

## Overview

WoodCraft Access Portal is a Flask-based demonstration application that implements Role-Based Access Control (RBAC). It uses Flask-Login for session management, Flask-Bcrypt for password hashing, and a CSV permission matrix to define role-based access.

The project demonstrates authentication, authorization, protected routes, and access-denied handling using four fictional user roles.

## Features

- Login and logout functionality.
- Password verification using bcrypt hashes.
- Four user roles with different permissions.
- Server-side access checks for protected routes.
- Custom HTTP 403 Forbidden page.
- CSV-based permission matrix.
- Password setup script that prompts securely without displaying passwords.
- Responsive HTML templates for the portal pages.

## Technology Stack

- Python
- Flask
- Flask-Login
- Flask-Bcrypt
- HTML and CSS
- JSON and CSV

## Project Structure

```text
woodcraft-access-control/
├── app.py
├── generate_users.py
├── set_demo_passwords.py
├── sample_users.json
├── role_permission_matrix.csv
├── README.md
├── .gitignore
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── dashboard.html
    ├── admin.html
    ├── inventory.html
    ├── orders.html
    ├── reports.html
    └── 403.html
```

## User Roles

| Role | Intended access |
|---|---|
| `admin` | User administration, inventory, orders, and reports. |
| `inventory_manager` | Inventory management and order processing. |
| `staff` | Inventory and order-related access. |
| `customer` | Dashboard and customer order access. |

Access is controlled by the role-permission matrix. Routes should deny access unless the corresponding permission is explicitly granted.

## Installation

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd woodcraft-access-control
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install Flask Flask-Login Flask-Bcrypt
```

### 4. Set up demo passwords

Run:

```bash
python set_demo_passwords.py
```

Follow the prompts to set a separate demo password for each fictional account. Use temporary passwords intended only for this project.

The script saves bcrypt password hashes in `sample_users.json`, not plaintext passwords.

### 5. Start the application

```bash
python app.py
```

Open the following address in your browser:

http://127.0.0.1:5000

Log in using one of the four demo usernames and the password you configured for that account.

## Application Routes

| Route | Purpose |
|---|---|
| `/` | Home page |
| `/login` | User authentication |
| `/logout` | End the authenticated session |
| `/dashboard` | Role dashboard |
| `/admin` | Administrative page |
| `/inventory` | Inventory page |
| `/orders` | Orders page |
| `/reports` | Reports page |

Unauthorized access is handled using a custom 403 Forbidden page.

## Permission Matrix

The `role_permission_matrix.csv` file defines permissions using these fields:

- `role`: the user's assigned role.
- `route`: the resource or route being evaluated.
- `permission`: `allow` or `deny`.
- `description`: the purpose of the rule.

The Flask application checks the permission matrix on the server side before rendering protected pages.

## Testing

The application has been manually tested with all four demo roles.

Testing should verify:

- Successful login with valid credentials.
- Rejection of invalid credentials.
- Access to routes permitted for each role.
- Denial of restricted routes.
- Logout and session protection.
- Correct handling of unauthorized requests.

## Security Notes and Limitations
- The accounts and application data are fictional and intended for demonstration.
Passwords are stored as bcrypt hashes.

Do not commit real passwords, production secrets, or personal data.

The default Flask secret key is for local development only. Configure a strong secret through the SECRET_KEY environment variable before deployment.

Run the application with debugging disabled in production.

Customer-specific order ownership and database-backed persistence would need further implementation before this could be used as a production application.

The project is an educational RBAC demonstration and has not been presented as a production-ready security system.

Author

WoodCraft Access Control — RBAC demonstration project.
## Automated Testing

The project includes automated access-control tests using pytest.

### Run Tests

```bash
python -m pytest -v
