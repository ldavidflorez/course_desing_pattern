from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from services.services import CategoryService
from di_container import Container

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET'])
@inject
def get_categories(category_service: CategoryService = Provide[Container.category_service]):
    token = request.headers.get("Authorization")
    if not category_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    return jsonify(category_service.get_all_categories())

@categories_bp.route('/categories/<int:category_id>', methods=['GET'])
@inject
def get_category(category_id, category_service: CategoryService = Provide[Container.category_service]):
    token = request.headers.get("Authorization")
    if not category_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    result = category_service.get_category_by_id(category_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)

@categories_bp.route('/categories', methods=['POST'])
@inject
def create_category(category_service: CategoryService = Provide[Container.category_service]):
    token = request.headers.get("Authorization")
    if not category_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"message": "Name is required"}), 400

    result = category_service.create_category(name)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result[0]), result[1]

@categories_bp.route('/categories', methods=['DELETE'])
@inject
def delete_category(category_service: CategoryService = Provide[Container.category_service]):
    token = request.headers.get("Authorization")
    if not category_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"message": "Name is required"}), 400

    result = category_service.delete_category(name)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result[0]), result[1]