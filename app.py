
import os

from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Development-only fallback. Set a strong environment secret.
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY",
    "development-only-change-this-secret"
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = 1800

# Demo accounts for this local lab.
users = {
    "alice": {
        "username": "alice",
        "role": "user",
        "password": generate_password_hash("alicepass")
    },
    "bob": {
        "username": "bob",
        "role": "support",
        "password": generate_password_hash("bobpass")
    },
    "admin": {
        "username": "admin",
        "role": "admin",
        "password": generate_password_hash("adminpass")
    }
}

created_users = []


# LOGIN
@app.post("/api/login")
def login():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "Username and password required"}), 400

    user = users.get(username)

    if user is None or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    session.clear()
    session["username"] = username

    session.permanent = True

    return jsonify({"message": "Login successful"}), 200


# LOGOUT
@app.post("/api/logout")
def logout():

    session.clear()

    return jsonify({"message": "Logged out"}), 200


def get_current_user():

    username = session.get("username")

    if not username:
        return None

    return users.get(username)


# ADMIN-ONLY FUNCTION
@app.post("/api/admin/create-user")
def create_user():

    current_user = get_current_user()

    # Authentication check
    if current_user is None:
        return jsonify({"error": "Authentication required"}), 401

    # Authorization check
    if current_user["role"] != "admin":
        return jsonify({"error": "Forbidden: Admin access required"}), 403

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")

    if not isinstance(username, str) or not username.strip():
        return jsonify({"error": "Valid username required"}), 400

    new_user = {
        "username": username.strip(),
        "role": "user"
    }

    created_users.append(new_user)

    return jsonify({
        "message": "User created",
        "user": new_user
    }), 201


if __name__ == "__main__":
    app.run(debug=True, port=5001)
