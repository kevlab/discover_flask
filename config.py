import os

# don't push config to git; just an example here
# use os.urandom(24) to generate a key and store key in environment var
# alt to load from file:
# with open('/etc/secret_key.txt') as f:
#     SECRET_KEY = f.read().strip()

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'o\xc6dG\x1eP\x04E\xd1\xe9\xc8\x8b\xbb\x06\x0e\x92\xcd\xfbn\xdb\xb1\xdf\xda\xaa'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class DevelopmentConfig(BaseConfig):
    DEBUG = True

# run this command in shell
# heroku config:set APP_SETTINGS=config.ProductionConfig --remote heroku
class ProductionConfig(BaseConfig):
    DEBUG = False  # really want to be explicit
