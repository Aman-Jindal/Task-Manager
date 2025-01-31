

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request, redirect, url_for
from models import db, Task


# Initialie Flask app
app = Flask(__name__)


# Configure Database (SQLite for Local development)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app)
migrate = Migrate(app, db)




# Home Route
@app.route('/')
def home():
    tasks = Task.query.all() # Fetch all tasks from the database
    return render_template('tasks.html', tasks=tasks)

# Add Task
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        # Get user input from here
        new_task = Task(
            title = request.form['title'],
            description = request.form['description']
        )
        db.session.add(new_task) # Add task to database
        db.session.commit() # Save changes
        return redirect(url_for('tasks')) # Redirect to task list
    
    # Retrieve all tasks from database
    all_tasks = Task.query.all()
    return render_template('tasks.html', tasks=all_tasks)

# Delete Task
@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id) # Fetch task by ID
    db.session.delete(task) # Remove from database
    db.session.commit()
    return redirect(url_for('tasks')) # Refresh page

# Mark Task as Completed
@app.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = True # Update status
    db.session.commit()
    return redirect(url_for('tasks'))


# Run the app
if __name__ == '__main__':
    with app.app_context(): # Ensures the app is in the correct context
        db.create_all() # Creates the database tables
    app.run(debug=True)
