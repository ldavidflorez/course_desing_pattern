from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from services.services import FavoriteService
from di_container import Container

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/favorites', methods=['GET'])
@inject
def get_favorites(favorite_service: FavoriteService = Provide[Container.favorite_service]):
    token = request.headers.get("Authorization")
    if not favorite_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    return jsonify(favorite_service.get_all_favorites())

@favorites_bp.route('/favorites', methods=['POST'])
@inject
def add_favorite(favorite_service: FavoriteService = Provide[Container.favorite_service]):
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
@inject
def remove_favorite(favorite_service: FavoriteService = Provide[Container.favorite_service]):
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