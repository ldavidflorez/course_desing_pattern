from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from services.services import FavoriteService
from di_container import Container
from .auth_decorators import token_required

favorites_bp = Blueprint("favorites", __name__)


@favorites_bp.route("/favorites", methods=["GET"])
@token_required
@inject
def get_favorites(
    favorite_service: FavoriteService = Provide[Container.favorite_service],
):
    return jsonify(favorite_service.get_all_favorites())


@favorites_bp.route("/favorites", methods=["POST"])
@token_required
@inject
def add_favorite(
    favorite_service: FavoriteService = Provide[Container.favorite_service],
):
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not all([user_id, product_id]):
        return jsonify({"message": "User ID and Product ID are required"}), 400

    result = favorite_service.add_favorite(user_id, product_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result[0]), result[1]


@favorites_bp.route("/favorites", methods=["DELETE"])
@token_required
@inject
def remove_favorite(
    favorite_service: FavoriteService = Provide[Container.favorite_service],
):
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not all([user_id, product_id]):
        return jsonify({"message": "User ID and Product ID are required"}), 400

    result = favorite_service.remove_favorite(user_id, product_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result[0]), result[1]
