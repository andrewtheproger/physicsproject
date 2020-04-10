from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(16))
    hints = db.relationship('Hint', backref='task', lazy='dynamic')

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'number': self.number,
            'hints': self.hints
        })


class Hint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    suggestions = db.relationship('Suggestion', backref='hint', lazy='dynamic')

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'task_id': self.task_id,
            'suggestions': self.suggestions
        })


class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hint_id = db.Column(db.Integer, db.ForeignKey('hint.id'))

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'hint_id': self.hint_id,
        })
