# Flask Product API

This Flask application provides a RESTful API for managing product information with basic CRUD operations. It includes functionality for creating, reading, updating, and deleting products. The app also features request validation, error handling, and centralized logging.

---

## Overview

The Product API allows you to manage a list of products with basic CRUD operations:
- **Create**: Add a new product to the database.
- **Read**: Retrieve a list of products or a single product by ID.
- **Update**: Modify an existing product.
- **Delete**: Remove a product from the database.

---

## Running the Application

The application runs on `http://localhost:5000` by default.

---

## API Endpoints

### 1. Create a Product

- **Endpoint**: `/products`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "name": "Product Name",
    "price": 19.99,
    "stock": 100,
    "description": "Optional description of the product"
  }
  ```

### 2. Get All Products

- **Endpoint**: `/products`
- **Method**: `GET`

### 3. Get a Product by ID

- **Endpoint**: `/products/<product_id>`
- **Method**: `GET`

### 4. Update a Product

- **Endpoint**: `/products/<product_id>`
- **Method**: `PUT`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "name": "Updated Product Name",
    "price": 29.99,
    "stock": 150,
    "description": "Updated description"
  }
  ```

### 5. Delete a Product

- **Endpoint**: `/products/<product_id>`
- **Method**: `DELETE`

---

## Sample Requests and Responses

### Create a Product

**Request**:
```bash
curl --location 'localhost:5001/products' \
--header 'Content-Type: application/json' \
--data '{
    "name" : "iPhone Cover",
    "price" : 50.0,
    "stock" : 10,
    "description" : "cover for iPhone 16"
}'
```

**Response**:
```json
{
    "data": {
        "product": {
            "description": "cover for iPhone 16",
            "name": "iPhone Cover",
            "price": 50.0,
            "stock": 10
        },
        "product_id": 1730657526689
    },
    "error": null,
    "message": "Product created successfully"
}
```

### Get All Products

**Request**:
```bash
curl --location --request GET 'localhost:5001/products' \
--header 'Content-Type: application/json' \
--data '{}'
```

**Response**:
```json
{
    "data": {
        "1730658722707": {
            "description": "cover for iPhone 16",
            "name": "iPhone Cover",
            "price": 50.0,
            "stock": 10
        }
    },
    "error": null,
    "message": null
}
```

### Get a Product by ID

**Request**:
```bash
curl --location --request GET 'localhost:5001/products/1730658722707' \
--header 'Content-Type: application/json' \
--data '{}'
```

**Response**:
```json
{
    "data": {
        "description": "cover for iPhone 16",
        "name": "iPhone Cover",
        "price": 50.0,
        "stock": 10
    },
    "error": null,
    "message": null
}
```

### Update a Product

**Request**:
```bash
curl --location --request PUT 'localhost:5001/products/1730658722707' \
--header 'Content-Type: application/json' \
--data '{
    "description": "cover for iPhone 16",
    "name": "iPhone 16 Cover",
    "price": 50.0,
    "stock": 10
}'
```

**Response**:
```json
{
    "data": {
        "product": {
            "description": "cover for iPhone 16",
            "name": "iPhone 16 Cover",
            "price": 50.0,
            "stock": 10
        },
        "product_id": 1730658722707
    },
    "error": null,
    "message": "Product updated successfully"
}
```

### Delete a Product

**Request**:
```bash
curl --location --request DELETE 'localhost:5001/products/1730658722707' \
--header 'Content-Type: application/json' \
--data '{}'
```

**Response**:
```json
{
    "data": null,
    "error": null,
    "message": "Product deleted successfully"
}
```