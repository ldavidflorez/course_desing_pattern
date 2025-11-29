from flask import Flask
from blueprints.auth_bp import auth_bp
from blueprints.products_bp import products_bp
from blueprints.categories_bp import categories_bp
from blueprints.favorites_bp import favorites_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(favorites_bp)

if __name__ == "__main__":
    app.run(debug=True)
