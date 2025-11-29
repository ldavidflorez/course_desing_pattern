from flask import Blueprint, request, jsonify
from services.services import FavoriteService
from repositories.json_repositories import JsonFavoriteRepository
from strategies.auth_strategies import TokenAuthStrategy

favorites_bp = Blueprint('favorites', __name__)

favorite_repo = JsonFavoriteRepository("db.json")
auth_strategy = TokenAuthStrategy()
favorite_service = FavoriteService(favorite_repo, auth_strategy)

@favorites_bp.route('/favorites', methods=['GET'])
def get_favorites():
    token = request.headers.get("Authorization")
    if not favorite_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    return jsonify(favorite_service.get_all_favorites())

@favorites_bp.route('/favorites', methods=['POST'])
def add_favorite():
    token = request.headers.get("Authorization")
    if not favorite_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not all([user_id, product_id]):
        return jsonify({"message": "User ID and Product ID are required"}), 400

    result = favorite_service.add_favorite(user_id, product_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result[0]), result[1]

@favorites_bp.route('/favorites', methods=['DELETE'])
def remove_favorite():
    token = request.headers.get("Authorization")
    if not favorite_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not all([user_id, product_id]):
        return jsonify({"message": "User ID and Product ID are required"}), 400

    result = favorite_service.remove_favorite(user_id, product_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result[0]), result[1]