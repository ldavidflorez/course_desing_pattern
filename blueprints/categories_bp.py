from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from services.services import CategoryService
from di_container import Container
from .auth_decorators import token_required

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/categories", methods=["GET"])
@token_required
@inject
def get_categories(
    category_service: CategoryService = Provide[Container.category_service],
):
    return jsonify(category_service.get_all_categories())


@categories_bp.route("/categories/<int:category_id>", methods=["GET"])
@token_required
@inject
def get_category(
    category_id, category_service: CategoryService = Provide[Container.category_service]
):
    result = category_service.get_category_by_id(category_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)


@categories_bp.route("/categories", methods=["POST"])
@token_required
@inject
def create_category(
    category_service: CategoryService = Provide[Container.category_service],
):
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"message": "Name is required"}), 400

    result = category_service.create_category(name)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result[0]), result[1]


@categories_bp.route("/categories", methods=["DELETE"])
@token_required
@inject
def delete_category(
    category_service: CategoryService = Provide[Container.category_service],
):
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"message": "Name is required"}), 400

    result = category_service.delete_category(name)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result[0]), result[1]
