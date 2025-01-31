# For Database Schema

from flask_sqlalchemy import SQLAlchemy

# Initializing the database
db = SQLAlchemy()

# Define Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Unique Task ID
    title = db.Column(db.String(100), nullable=False) # Task Title
    description = db.Column(db.Text, nullable=True) # Task Description
    

    def __repr__(self):
        return f'<Task {self.title}>'