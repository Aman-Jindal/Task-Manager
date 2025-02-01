

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from models import db, Task
from forms import TaskForm
from datetime import datetime
import os
from dotenv import load_dotenv


# Load environment variables from .env (if you have one)
load_dotenv()


# Initialie Flask app
app = Flask(__name__, static_folder='static')


# Configure Database (SQLite for Local development)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecret') # For Flask-WTF


# Initialize Database
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context(): # Ensures the app is in the correct context
    db.create_all() # Creates the database tables



# Home Route
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all() # Fetch all tasks from the database
    return render_template('index.html', task=tasks)

# Add Task
@app.route('/tasks', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data if form.due_date.data else None,
            is_complete=form.is_complete.raw_data
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_task.html', form=form)


# Edit Task
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data if form.due_date.data else None
        task.is_complete = form.is_complete.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_task.html', form=form, task=task)

# Delete Task
@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id) # Fetch task by ID
    db.session.delete(task) # Remove from database
    db.session.commit()
    flash('Task deleted successfully!', 'danger')
    return redirect(url_for('index')) # Refresh page

# Mark Task as Completed
@app.route('/toggle_complete/<int:id>', methods=['POST'])
def toggle_complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_complete = not task.is_complete # Update status
    db.session.commit()
    # For AJAX requests, you can return a JSON response
    return jsonify({'status':'success', 'is_complete': task.is_complete})


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
