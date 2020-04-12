from flask_sqlalchemy import SQLAlchemy
import json
import jwt
import datetime
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.BigInteger)
    updated_date = db.Column(db.BigInteger)
    number = db.Column(db.String(16), unique=True)
    latex = db.Column(db.String(4096))
    image_hrefs_json = db.Column(db.String(4096))
    hints = db.relationship('Hint', backref='task', lazy='dynamic')

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
            'number': self.number,
            'latex': self.latex,
            'image_hrefs_json': self.image_hrefs_json,
            'hints': self.hints
        })


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
    image_hrefs_json = db.Column(db.String(4096))
    status = db.Column(db.Enum(HintStatus))

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
            'task_id': self.task_id,
            'latex': self.latex,
            'status': self.status,
            'image_hrefs_json': self.image_hrefs_json
        })


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.BigInteger)
    updated_date = db.Column(db.BigInteger)
    login = db.Column(db.String(256), unique=True)
    password_hash = db.Column(db.String(128))  # hash stores as string
    role = db.Column(db.Enum(UserRole))
    auth_token = db.Column(db.String(512))  # jwt has no max length, but 512 is fine for now

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
            'login': self.login,
            'role': self.role.value
        })

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id, secret):
        now = datetime.datetime.utcnow()

        payload = {
            'exp': now + datetime.timedelta(days=0, seconds=500),
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
