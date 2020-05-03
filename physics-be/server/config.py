import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'vol/server.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
SECRET_JWT_KEY = 'SECRET_JWT_KEY'  # todo
SECURITY_PASSWORD_SALT = 'SECURITY_PASSWORD_SALT'  # todo

DISCORD_WEBHOOK = 'https://discordapp.com/api/webhooks/704063734523363437/l1HMbIYCjePSkiXHilXuNAXBmSLQ1XNhvJ_com5Bq1uvXAV20jhcVeh06Fo1hvPxBLva'
