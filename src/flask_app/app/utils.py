from datetime import datetime


# In-memory database for storing product data
in_memory_db = {}


def generate_product_id():
    """
    Generate a unique product ID based on the current timestamp.
    This is a simple method for generating IDs in an in-memory DB.
    """
    return int(datetime.now().timestamp() * 1000)


def validate_product_data(product_data):
    """
    A utility function for additional custom validation on product data.
    Can be used for validations not covered by Marshmallow schemas.
    """
    required_fields = ['name', 'price', 'stock']
    missing_fields = [field for field in required_fields if field not in product_data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")


# Helper function for JSON response formatting
def format_response(data=None, message=None, error=None, status_code=200):
    """
    Utility to format JSON responses consistently across the API.
    """
    response = {
        'data': data,
        'message': message,
        'error': error
    }
    return response, status_code
