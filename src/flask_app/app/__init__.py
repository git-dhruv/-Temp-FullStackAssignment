from flask import Flask, g, request
import logging
import time

from flask_app.app.routes import product_bp
from flask_app.app.error_handlers import register_error_handlers
from flask_app.app.utils import format_response


def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(product_bp)

    # Register error handlers
    register_error_handlers(app)

    # Loggers
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    @app.before_request
    def log_request():
        g.start_time = time.time()
        logging.info("Request: %s %s - Body: %s", request.method, request.path, request.get_json())

    @app.after_request
    def log_response(response):
        duration = time.time() - g.start_time
        logging.info(f"Response: {response.status_code} - Body: {response.get_data(as_text=True)} - Duration: {duration:.3f}s")
        return response

    @app.teardown_request
    def log_exception(error=None):
        if error:
            logging.error("Error: %s", str(error))
            return format_response(error="Internal server error", status_code=500)

    return app