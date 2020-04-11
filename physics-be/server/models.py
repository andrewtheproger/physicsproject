from flask_sqlalchemy import SQLAlchemy
import json
import enum

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.BigInteger)
    updated_date = db.Column(db.BigInteger)
    number = db.Column(db.String(16))
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
