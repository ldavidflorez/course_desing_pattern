from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from strategies.auth_strategies import TokenAuthStrategy
from di_container import Container

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth", methods=["POST"])
@inject
def login(auth_strategy: TokenAuthStrategy = Provide[Container.auth_strategy]):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "student" and password == "desingp":
        token = auth_strategy.valid_token
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "unauthorized"}), 401
