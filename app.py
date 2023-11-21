from datetime import datetime, timedelta

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import jinja_partials
import task
import json
from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, StringField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    project = StringField('Project', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    due_date = DateTimeLocalField('Due Date', validators=[DataRequired()])
    submit = SubmitField('Add Task')


app = Flask(__name__)
app.config.from_file("secrets_config", load=json.load)
jinja_partials.register_extensions(app)


def find_end(date: datetime, date_range: str) -> int:
    """Find difference to end of the month."""
    if date_range == "month":
        if date.day in [1, 3, 5, 7, 8, 10, 12]:
            return 31 - date.day
        elif date.day == 2:
            return 28 - date.day
        else:
            return 30 - date.day


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/tasks', methods=["GET", "POST"])
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        print(form.due_date.data)
        print(type(form.due_date.data))
        task.add_task(task_description=form.task.data, task_project=form.project.data,
                      tags=form.tags.data, due_date=form.due_date.data)
        return redirect(url_for('tasks'))

    starting_tasks = task.task_list_pending(None)
    return render_template('tasks.html', tasks=starting_tasks, form=form)


@app.route('/overdue', methods=["GET", "POST"])
def overdue():
    if request.args:
        task.mark_task_completed(request.args['task_id'])
    overdue_tasks = task.task_list_overdue()
    return render_template('partials/task_table.html', tasks=overdue_tasks, tab="overdue")


@app.route('/due-today', methods=["GET", "POST"])
def due_today():
    """The tasks that have a due date of today."""
    if request.args:
        task.mark_task_completed(request.args['task_id'])
    today = datetime.today()
    today_tasks = task.task_list_pending(today)
    return render_template('partials/task_table.html', tasks=today_tasks, tab="due-today")


@app.route('/due-this-month', methods=["GET", "POST"])
def due_this_month():
    if request.args:
        task.mark_task_completed(request.args['task_id'])
    today = datetime.today().astimezone()
    month_tasks = task.task_list_pending(today - timedelta(today.day), today + timedelta(find_end(today, "month")))
    return render_template('partials/task_table.html', tasks=month_tasks, tab='due-this-month')


@app.route('/all-incomplete', methods=["GET", "POST"])
def all_incomplete():
    if request.args:
        task.mark_task_completed(request.args['task_id'])
    all_incomplete_tasks = task.task_list_pending(None)
    return render_template('partials/task_table.html', tasks=all_incomplete_tasks, tab='all-incomplete')


@app.route('/completed')
def completed():
    completed_tasks = task.task_list_completed()
    return render_template('partials/task_table.html', tasks=completed_tasks)


if __name__ == '__main__':
    app.run()
