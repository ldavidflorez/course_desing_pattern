from flask import Blueprint, request, jsonify
from strategies.auth_strategies import TokenAuthStrategy

auth_bp = Blueprint('auth', __name__)
auth_strategy = TokenAuthStrategy()

@auth_bp.route('/auth', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "student" and password == "desingp":
        token = "abcd12345"  # In a real app, generate JWT
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "unauthorized"}), 401