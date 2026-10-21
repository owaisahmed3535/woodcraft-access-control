# Woodcraft Access Control

## Overview

This project defines a role-permission matrix and fictional sample user data for a mock Woodcraft application. It demonstrates role-based access control (RBAC) concepts and secure password hashing with bcrypt.

## Project Files

- `role_permission_matrix.csv` — maps application roles to routes and their allowed or denied permissions.
- `generate_users.py` — generates fictional user records and hashes randomly generated temporary passwords using bcrypt.
- `sample_users.json` — contains four fictional users with bcrypt password hashes only.

## Roles and Permissions

| Role | Access |
|---|---|
| `admin` | Manages users, inventory, orders, and reports. |
| `inventory_manager` | Views and updates inventory and accesses orders for stock processing. Cannot manage users or view reports. |
| `staff` | Views inventory and assigned order information. Cannot manage users or view reports. |
| `customer` | Views the homepage, own account dashboard, and own orders. Cannot access internal inventory, user management, or reports. |

## Permission Mapping

The CSV file uses these fields:

- `role` — the user role being evaluated.
- `route` — the application route.
- `permission` — `allow` or `deny`.
- `description` — explains the intended access rule.

An `allow` entry represents intended access, while a `deny` entry represents prohibited access. Applications should enforce these permissions on the server side and deny access by default when a rule is missing. Customer order access must be restricted to that customer's own records.

## Sample Users and Password Security

The sample dataset contains four fictional accounts. Email addresses use the reserved `example.com` domain and do not represent real users.

Passwords are generated temporarily and hashed using bcrypt with a work factor of 12. Only the resulting hashes are saved in `sample_users.json`; the temporary passwords are not stored.

To generate or regenerate the sample dataset, activate your Python virtual environment, install the dependency, and run:

```bash
python -m pip install bcrypt
python generate_users.py
```

Regenerating the dataset creates new password hashes.

## Limitations

This project is a demonstration dataset and permission design, not a complete authentication system. It does not implement login, sessions, or route enforcement. The permissions must be integrated into an application before they provide actual access control.

No real personal information or production credentials are included.
