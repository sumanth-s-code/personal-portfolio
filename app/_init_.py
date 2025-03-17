"""
Application factory for the Personal Portfolio app with Admin Panel.

This module creates and configures the Flask application.
"""

from flask import Flask
import os

def create_app(test_config=None):
    """
    Create and configure the Flask app.

    Args:
        test_config (dict, optional): Configuration dictionary for testing.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',  # Change this in production!
        DATABASE=os.path.join(app.instance_path, 'portfolio.sqlite'),
        ADMIN_USERNAME='admin',
        ADMIN_PASSWORD='password'  # Change for production!
    )
    
    if test_config:
        app.config.update(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database
    from . import db
    db.init_app(app)

    # Register blueprints for public routes, admin panel, and authentication.
    from . import routes
    app.register_blueprint(routes.bp)

    from . import admin
    app.register_blueprint(admin.bp, url_prefix='/admin')

    from . import auth
    app.register_blueprint(auth.bp)

    return app