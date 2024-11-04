from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class ProductSchema(Schema):
    """
    Schema for validating product data.
    """
    name = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Product name is required."}
    )
    price = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        error_messages={"required": "Price is required.", "invalid": "Price must be a valid number."}
    )
    stock = fields.Integer(
        required=True,
        validate=validate.Range(min=0),
        error_messages={"required": "Stock is required.", "invalid": "Stock must be a valid integer."}
    )
    description = fields.String(
        validate=validate.Length(max=500),
        missing="",
        error_messages={"invalid": "Description must be a string."}
    )

    @validates("name")
    def validate_name(self, value):
        if not re.match("^[A-Za-z0-9 ]+$", value):
            raise ValidationError("Product name must contain only letters, numbers, and spaces.")


    @validates("price")
    def validate_price(self, value):
        if value < 0:
            raise ValidationError("Price must be a positive number.")

    @validates("stock")
    def validate_stock(self, value):
        if value < 0:
            raise ValidationError("Stock must be a non-negative integer.")


# Instantiate the schema for use in routes
product_schema = ProductSchema()
