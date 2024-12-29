from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    habits = db.relationship('Habit', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return True

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    growth = db.Column(db.Integer, default=0)
    points = db.relationship('HabitPoint', back_populates='habit', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


from datetime import datetime

class HabitPoint(db.Model):
    __tablename__ = 'habit_points'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    habit = db.relationship('Habit', back_populates='points')

    def __repr__(self):
        return f"<HabitPoint(id={self.id}, habit_id={self.habit_id}, x={self.x}, y={self.y})>"
