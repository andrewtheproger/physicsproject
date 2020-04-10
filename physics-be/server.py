from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


def to_model_list(tasks):
    return [to_model(t) for t in tasks]


def to_model(task):
    return {
        'id': task.id,
        'number': task.number
    }

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_MIGRATE_REPO"] = SQLALCHEMY_MIGRATE_REPO

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.String(16))

    def __repr__(self):
        return '<User %r>' % self.number


@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok'}


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Tasks.query.all()
    return jsonify(to_model_list(tasks))


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Tasks.query.get(task_id)
    if not task:
        abort(404)
    return jsonify(to_model(task))


if __name__ == '__main__':
    app.run(debug=True)
