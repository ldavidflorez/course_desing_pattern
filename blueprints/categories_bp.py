from flask import Blueprint, request, jsonify
from services.services import CategoryService
from repositories.json_repositories import JsonCategoryRepository
from strategies.auth_strategies import TokenAuthStrategy

categories_bp = Blueprint('categories', __name__)

category_repo = JsonCategoryRepository("db.json")
auth_strategy = TokenAuthStrategy()
category_service = CategoryService(category_repo, auth_strategy)

@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    token = request.headers.get("Authorization")
    if not category_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    return jsonify(category_service.get_all_categories())

@categories_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    token = request.headers.get("Authorization")
    if not category_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    result = category_service.get_category_by_id(category_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)

@categories_bp.route('/categories', methods=['POST'])
def create_category():
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
def delete_category():
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