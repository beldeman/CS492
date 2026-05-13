from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import hashlib
import json
import re
import os

app = Flask(__name__)
app.secret_key = "replace-this-with-a-secure-key"

DATA_DIR = Path(os.getenv('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'PizzaShop'
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATA_FILE = DATA_DIR / 'users.json'
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def load_users():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError:
            return []


def save_users(users):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as handle:
        json.dump(users, handle, indent=2)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def find_user_by_email(email: str):
    email = email.strip().lower()
    return next((user for user in load_users() if user["email"] == email), None)


def validate_registration_form(form):
    full_name = form.get("full_name", "").strip()
    email = form.get("email", "").strip().lower()
    phone = form.get("phone", "").strip()
    address = form.get("address", "").strip()
    password = form.get("password", "")
    confirm_password = form.get("confirm_password", "")

    if not full_name:
        return False, "Full name is required."
    if not email or not EMAIL_REGEX.match(email):
        return False, "Please enter a valid email address."
    if find_user_by_email(email):
        return False, "An account already exists with that email."
    if not phone:
        return False, "Phone number is required."
    if not address:
        return False, "Address is required."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if password != confirm_password:
        return False, "Passwords do not match."
    return True, {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "address": address,
        "password": password,
    }


def get_current_user():
    email = session.get("user_email")
    if not email:
        return None
    return find_user_by_email(email)


@app.route("/")
def home():
    return render_template("index.html", user=get_current_user())


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_email"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        valid, result = validate_registration_form(request.form)
        if valid:
            new_user = {
                "full_name": result["full_name"],
                "email": result["email"],
                "phone": result["phone"],
                "address": result["address"],
                "password_hash": hash_password(result["password"]),
            }
            users = load_users()
            users.append(new_user)
            save_users(users)
            flash("Your account has been created successfully.", "success")
            return redirect(url_for("login"))
        flash(result, "error")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_email"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = find_user_by_email(email)
        if user and user["password_hash"] == hash_password(password):
            session["user_email"] = user["email"]
            flash(f"Welcome back, {user['full_name']}!", "success")
            return redirect(url_for("home"))
        flash("Email or password is incorrect.", "error")
    return render_template("login.html")


@app.route("/profile")
def profile():
    user = get_current_user()
    if not user:
        flash("Please log in to view your profile.", "error")
        return redirect(url_for("login"))
    return render_template("profile.html", user=user)


@app.route("/logout")
def logout():
    session.pop("user_email", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/api/check-email")
def api_check_email():
    email = request.args.get("email", "").strip().lower()
    exists = bool(find_user_by_email(email))
    return jsonify({"exists": exists})


if __name__ == "__main__":
    app.run(debug=True)
