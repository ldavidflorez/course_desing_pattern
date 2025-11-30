from flask import Flask
from blueprints.auth_bp import auth_bp
from blueprints.products_bp import products_bp
from blueprints.categories_bp import categories_bp
from blueprints.favorites_bp import favorites_bp
from di_container import Container

app = Flask(__name__)

# Initialize DI container
container = Container()
container.wire()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(favorites_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
