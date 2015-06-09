import os

# don't push config to git; just an example here
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "a secret"
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False  # really want to be explicit
