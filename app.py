from flask import Flask
from models import db, init_models
from controllers.main import main_bp
from controllers.auth import auth_bp
from controllers.admin import admin_bp
from controllers.user import user_bp
from utils import create_admin
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = '3d7a44959689295302db6b362b049ed1c2ef3daeab84a5c0d878ea999f8f7a7a'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    # Initialize models
    with app.app_context():
        init_models()
        db.create_all()
        create_admin()
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
