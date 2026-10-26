import csv
import json
import os
from pathlib import Path

from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_bcrypt import Bcrypt

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-only-change-this-before-deployment"
)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."

# Load sample users from JSON.
with open(BASE_DIR / "sample_users.json", encoding="utf-8") as file:
    USERS = json.load(file)

USERS_BY_USERNAME = {user["username"]: user for user in USERS}

# Load the role-permission matrix from CSV.
PERMISSIONS = set()

with open(BASE_DIR / "role_permission_matrix.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        PERMISSIONS.add(
            (row["role"], row["route"], row["permission"].lower())
        )


class PortalUser(UserMixin):
    def __init__(self, record):
        self.id = record["username"]
        self.username = record["username"]
        self.role = record["role"]
        self.password_hash = record["password_hash"]


@login_manager.user_loader
def load_user(username):
    record = USERS_BY_USERNAME.get(username)
    if record:
        return PortalUser(record)
    return None


def role_allows(route):
    """Allow only routes explicitly marked allow for the user's role."""
    return (current_user.role, route, "allow") in PERMISSIONS


def require_role_permission(route):
    if not current_user.is_authenticated:
        return redirect(url_for("login", next=request.path))

    if not role_allows(route):
        abort(403)

    return None


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        record = USERS_BY_USERNAME.get(username)

        if record and bcrypt.check_password_hash(
            record["password_hash"], password
        ):
            user = PortalUser(record)
            login_user(user)

            next_page = request.args.get("next", "")
            if next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    denied = require_role_permission("/dashboard")
    if denied:
        return denied

    return render_template("dashboard.html")


@app.route("/admin")
@login_required
def admin():
    # The existing matrix protects /users for administrators.
    denied = require_role_permission("/users")
    if denied:
        return denied

    return render_template("admin.html")


@app.route("/inventory")
@login_required
def inventory():
    denied = require_role_permission("/inventory")
    if denied:
        return denied

    return render_template("inventory.html")


@app.route("/orders")
@login_required
def orders():
    denied = require_role_permission("/orders")
    if denied:
        return denied

    return render_template("orders.html")


@app.route("/reports")
@login_required
def reports():
    denied = require_role_permission("/reports")
    if denied:
        return denied

    return render_template("reports.html")


@app.errorhandler(403)
def forbidden(_error):
    return render_template("403.html"), 403


if __name__ == "__main__":
    app.run(debug=True)
