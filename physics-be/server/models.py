from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(16))

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'number': self.number,
        })
