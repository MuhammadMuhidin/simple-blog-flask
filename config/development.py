import os
from config.default import DefaultConfig

class DevelopmentConfig(DefaultConfig):
    """
    Development configuration settings for the application.
    Inherits from DefaultConfig and overrides specific settings.
    """
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_DEV')