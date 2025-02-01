# For Database Schema

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initializing the database
db = SQLAlchemy()

# Define Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Unique Task ID
    title = db.Column(db.String(100), nullable=False) # Task Title
    description = db.Column(db.Text, nullable=True) # Task Description
    priority = db.Column(db.String(10), nullable=False, default='Medium') # Options: Low, Medium, High
    due_date = db.Column(db.Date)
    is_complete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return f'<Task {self.id} - {self.title}>'