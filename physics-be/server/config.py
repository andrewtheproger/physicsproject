import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'server.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
SECRET_JWT_KEY = 'SECRET_JWT_KEY'  # todo
SECURITY_PASSWORD_SALT = 'SECURITY_PASSWORD_SALT'  # todo
