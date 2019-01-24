"""
Api configurations
"""
import os

class Config:
    """
    Base configuration class.
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_URL_TEST = os.getenv('DATABASE_URL_TEST')

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """
    Testing Configurations, with a separate test database
    """
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False


APP_CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': TestingConfig
}
