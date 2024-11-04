"""Product management API using Flask, handling CRUD operations with in-memory storage."""

from flask import Blueprint, request
from marshmallow import ValidationError

from flask_app.app.schemas import product_schema
from flask_app.app.utils import (
    in_memory_db,
    format_response,
    validate_product_data,
    generate_product_id
)

# Blueprint and DB
product_bp = Blueprint('products', __name__, url_prefix='/products')
products = in_memory_db


# Create a new product
@product_bp.route('', methods=['POST'])
def create_product():
    try:
        # Parse and validate JSON data
        product_data = request.get_json()
        validate_product_data(product_data)

        # Validate using Marshmallow schema
        product_data = product_schema.load(product_data)

        # Generate a unique ID and save the product
        product_id = generate_product_id()
        products[product_id] = product_data
        return format_response(
            data={'product_id': product_id, 'product': product_data},
            message="Product created successfully",
            status_code=201
        )
    except ValidationError as err:
        # Handle schema validation errors
        return format_response(error=err.messages, status_code=400)
    except ValueError as ve:
        # Handle custom validation errors
        return format_response(error=str(ve), status_code=400)
    except Exception as e:
        # Log and return a generic error message
        return format_response(error="Internal server error", status_code=500)


# Retrieve all products
@product_bp.route('', methods=['GET'])
def get_products():
    try:
        return format_response(data=products, status_code=200)
    except Exception as e:
        return format_response(error="Internal server error", status_code=500)


# Retrieve a specific product by ID
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = products.get(product_id)
        if not product:
            return format_response(error="Product not found", status_code=404)
        return format_response(data=product, status_code=200)
    except Exception as e:
        return format_response(error="Internal server error", status_code=500)


# Update an existing product by ID
@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        if product_id not in products:
            return format_response(error="Product not found", status_code=404)

        updated_data = request.get_json()
        validate_product_data(updated_data)

        updated_data = product_schema.load(updated_data)

        products[product_id].update(updated_data)
        return format_response(
            data={'product_id': product_id, 'product': products[product_id]},
            message="Product updated successfully",
            status_code=200
        )
    except ValidationError as err:
        return format_response(error=err.messages, status_code=400)
    except ValueError as ve:
        return format_response(error=str(ve), status_code=400)
    except Exception as e:
        return format_response(error="Internal server error", status_code=500)


# Delete a product by ID
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        if product_id not in products:
            return format_response(error="Product not found", status_code=404)
        del products[product_id]
        return format_response(
            message="Product deleted successfully",
            status_code=200
        )
    except Exception as e:
        return format_response(error="Internal server error", status_code=500)
