from flask import Flask, current_app
from flask_migrate import Migrate
import os

def create_app():
    # Create Flask application instance
    app = Flask(__name__,instance_relative_config=True)

    # Load config based on the environment variable
    env = os.environ.get('FLASK_ENV')
    print(f"Current environment: {env.upper()}")
    
    # Set the configuration based on the environment
    if env == 'Production':
        app.config.from_object('config.production.ProductionConfig')
    elif env == 'Development':
        app.config.from_object('config.development.DevelopmentConfig')

    # Initialize the database
    from .db import db
    db.init_app(app)

    from .models import User, Post
    Migrate(app, db)

    # Context processor to inject the blog title into templates
    @app.context_processor
    def inject_blog_title():
        blog_header = 'Blog with Flask'
        if os.environ.get("FLASK_ENV") == "Production":
            blog_header += ' - Production'
        elif os.environ.get("FLASK_ENV") == "Development":
            blog_header += ' - Development'
        return dict(blog_header=blog_header)

    # Register blueprints
    from .blog import bp as blog_bp
    app.register_blueprint(blog_bp)
    app.add_url_rule('/', endpoint='index')

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app