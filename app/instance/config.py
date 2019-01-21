"""
Api configurations
"""

class Config:
    """
    Base configuration class.
    """
    DEBUG = False
    TESTING = False

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
