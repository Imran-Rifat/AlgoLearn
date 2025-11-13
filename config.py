import os
from datetime import timedelta


class Config:
    """Application configuration"""

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')

    # Redis Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

    # Rate Limiting
    RATE_LIMIT_STORAGE_URL = os.getenv('RATE_LIMIT_STORAGE_URL', 'memory://')

    # Cache Configuration
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))

    # API Configuration
    API_VERSION = 'v1'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Learning Configuration
    SUPPORTED_LANGUAGES = ['python', 'java', 'javascript', 'cpp', 'csharp']
    DEFAULT_LANGUAGE = 'python'
    MAX_QUESTION_LEVEL = 10
    MIN_QUESTION_LEVEL = 1


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://yourdomain.com').split(',')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get appropriate configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])