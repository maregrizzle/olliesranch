from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=False)
    isCompleted = db.Column(db.Boolean, default=False, nullable=False)
    category = db.Column(db.String(20), nullable=False)  # 'Daily' or 'Weekly'
    subcategory = db.Column(db.String(20), nullable=True)  # New for "Animals" or "Home"
    details = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, default=0)
    time_of_day = db.Column(db.String(20), nullable=True)
    day_of_week = db.Column(db.String(20), nullable=True)  # New for specifying days for weekly tasks
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'isCompleted': self.isCompleted,
            'category': self.category,
            'subcategory': self.subcategory,
            'details': self.details,
            'order': self.order,
            'time_of_day': self.time_of_day,
            'day_of_week': self.day_of_week
        }

# Create the database tables before the first request
with app.app_context():
    db.create_all()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    category = request.args.get('category', None)
    subcategory = request.args.get('subcategory', None)
    tasks_query = Task.query
    if category:
        tasks_query = tasks_query.filter_by(category=category)
    if subcategory:
        tasks_query = tasks_query.filter_by(subcategory=subcategory)
    tasks = tasks_query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/task', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(
        description=data['description'],
        details=data.get('details', ''),
        category=data['category'],
        subcategory=data.get('subcategory', None),
        time_of_day=data.get('time_of_day', None),
        day_of_week=data.get('day_of_week', None),
        order=data.get('order', 0),
        isCompleted=data.get('isCompleted', False)
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        data = request.json
        for key, value in data.items():
            setattr(task, key, value)
        db.session.commit()
        return jsonify(task.to_dict())
    return jsonify({'message': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
