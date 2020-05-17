from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
import enum
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.BigInteger)
    updated_date = db.Column(db.BigInteger)
    url = db.Column(db.String(256))
    thumbnail_url = db.Column(db.String(256))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)
  

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.BigInteger)
    updated_date = db.Column(db.BigInteger)
    base_number = db.Column(db.String(16))
    task_number = db.Column(db.String(16))
    latex = db.Column(db.String(4096))
    hints = db.relationship('Hint', backref='task', lazy='dynamic')
    image_ids_json = db.Column(db.String(4096))
    images = db.relationship('Image', lazy=True)


class HintStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    declined = "declined"


class UserRole(enum.Enum):
    user = "user"
    admin = "admin"


class Hint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.BigInteger)
    updated_date = db.Column(db.BigInteger)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    latex = db.Column(db.String(4096))
    image_ids_json = db.Column(db.String(4096))
    status = db.Column(db.Enum(HintStatus))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.BigInteger)
    updated_date = db.Column(db.BigInteger)
    email = db.Column(db.String(256), unique=True)
    password_hash = db.Column(db.String(128))  # hash stores as string
    role = db.Column(db.Enum(UserRole))
    auth_token = db.Column(db.String(512))  # jwt has no max length, but 512 is fine for now
    color_background_primary = db.Column(db.String(16))  # sqlalchemy ColorType is fine but
    color_background_secondary = db.Column(db.String(16))  # sqlalchemy breaks the `flask db upgrade` flow
    color_foreground_primary = db.Column(db.String(16))  # see https://github.com/miguelgrinberg/Flask-Migrate/issues/62
    color_foreground_secondary = db.Column(db.String(16))

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id, secret):
        now = datetime.datetime.utcnow()

        payload = {
            'exp': now + datetime.timedelta(days=0, seconds=2 * 3600),  # todo increase login time by adding salt to the user_id
            'iat': now,
            'sub': user_id
        }

        return jwt.encode(
            payload,
            secret,
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(auth_token, secret):
        return jwt.decode(auth_token, secret)
