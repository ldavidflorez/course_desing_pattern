from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from services.services import ProductService
from di_container import Container

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
@inject
def get_products(product_service: ProductService = Provide[Container.product_service]):
    token = request.headers.get("Authorization")
    if not product_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    category_filter = request.args.get("category")
    if category_filter:
        return jsonify(product_service.get_products_by_category(category_filter))

    return jsonify(product_service.get_all_products())

@products_bp.route('/products/<int:product_id>', methods=['GET'])
@inject
def get_product(product_id, product_service: ProductService = Provide[Container.product_service]):
    token = request.headers.get("Authorization")
    if not product_service.authenticate(token):
        return jsonify({"message": "Unauthorized invalid token"}), 401

    result = product_service.get_product_by_id(product_id)
    if isinstance(result, tuple):  # Error case
        return jsonify(result[0]), result[1]
    return jsonify(result)

@products_bp.route('/products', methods=['POST'])
@inject
def create_product(product_service: ProductService = Provide[Container.product_service]):
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