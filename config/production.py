import os
from config.default import DefaultConfig

class ProductionConfig(DefaultConfig):
    """
    Production configuration settings for the application.
    Inherits from DefaultConfig and overrides specific settings.
    """
    
    DEBUG = False
    SQLALCHEMY_DATABASE_URI  = os.environ.get('SQLALCHEMY_DATABASE_URI_PROD')