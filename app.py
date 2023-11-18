from datetime import datetime

from flask import Flask
from flask import render_template
import jinja_partials
import task

app = Flask(__name__)

jinja_partials.register_extensions(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/tasks')
def tasks():
    starting_tasks = task.task_list_pending(None)
    return render_template('tasks.html', tasks=starting_tasks)

@app.route('/overdue')
def overdue():
    overdue_tasks = task.task_list_overdue()
    return render_template('partials/task_table.html', tasks=overdue_tasks)

@app.route('/due-today')
def due_today():
    """The tasks that have a due date of today."""
    today = datetime.today()
    today_tasks = task.task_list_pending(today)
    return render_template('partials/task_table.html', tasks=today_tasks)


@app.route('/all-incomplete')
def all_incomplete():
    all_incomplete_tasks = task.task_list_pending(None)
    return render_template('partials/task_table.html', tasks=all_incomplete_tasks)


if __name__ == '__main__':
    app.run()
