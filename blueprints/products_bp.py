from flask import Blueprint, request, jsonify
from services.services import ProductService
from repositories.json_repositories import JsonProductRepository, JsonCategoryRepository
from strategies.auth_strategies import TokenAuthStrategy

products_bp = Blueprint('products', __name__)

# Dependency Injection setup (simple, could use a DI container)
product_repo = JsonProductRepository("db.json")
category_repo = JsonCategoryRepository("db.json")
auth_strategy = TokenAuthStrategy()
product_service = ProductService(product_repo, category_repo, auth_strategy)

@products_bp.route('/products', methods=['GET'])
def get_products():
    token = request.headers.get("Authorization")
    if not product_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    category_filter = request.args.get("category")
    if category_filter:
        return jsonify(product_service.get_products_by_category(category_filter))

    return jsonify(product_service.get_all_products())

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    token = request.headers.get("Authorization")
    if not product_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    result = product_service.get_product_by_id(product_id)
    if isinstance(result, tuple):  # Error case
        return jsonify(result[0]), result[1]
    return jsonify(result)

@products_bp.route('/products', methods=['POST'])
def create_product():
    token = request.headers.get("Authorization")
    if not product_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    data = request.get_json()
    name = data.get("name")
    category = data.get("category")
    price = data.get("price")

    if not all([name, category, price]):
        return jsonify({"message": "Name, category, and price are required"}), 400

    result = product_service.create_product(name, category, price)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result[0]), result[1]