from datetime import datetime, timedelta

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask_login import LoginManager, login_required, login_user, UserMixin
import jinja_partials
import task
import json
from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, StringField, SubmitField, HiddenField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash


class TaskForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    project = StringField('Project', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    due_date = DateTimeLocalField('Due Date', validators=[DataRequired()])
    uuid = HiddenField()
    submit = SubmitField('Add Task')
    modify = SubmitField("Modify Task")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep Me Logged In')
    submit = SubmitField('Login')


class User(UserMixin):
    pass

app = Flask(__name__)
app.config.from_file("secrets_config", load=json.load)
jinja_partials.register_extensions(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


def find_end(date: datetime, date_range: str) -> int:
    """Find difference to end of the month."""
    if date_range == "month":
        if date.day in [1, 3, 5, 7, 8, 10, 12]:
            return 31 - date.day
        elif date.day == 2:
            return 28 - date.day
        else:
            return 30 - date.day


@login_manager.user_loader
def load_user(user_id):
    with open("secrets_config", "r") as file:
        secrets = json.load(file)
    if user_id not in secrets["user"]:
        print("Username not found!")
    user = User()
    user.id = user_id
    return user


def verify_password(user: str, password: str):
    with open("secrets_config", "r") as file:
        secrets = json.load(file)
        return check_password_hash(secrets["user"][user]["password"], password)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(form.username.data)
        if verify_password(user.get_id(), form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('index')
            return redirect(next)
    return render_template('login.html', form=form)


@app.route('/modify_task', methods=["POST"])
@login_required
def modify_task():
    filled_out_form = TaskForm()
    if request.args:
        this_task = task.get_task(request.args['task_id'])
        tags = " ".join(this_task.tags)
        filled_out_form = TaskForm(task=this_task.description, project=this_task.project, tags=tags,
                                   due_date=this_task.due, uuid=request.args['task_id'])
        return render_template('partials/add_task.html', form=filled_out_form, modify=True)


@app.route('/tasks', methods=["GET", "POST"])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        if form.submit.data:
            task.add_task(task_description=form.task.data, task_project=form.project.data,
                          tags=form.tags.data, due_date=form.due_date.data)
        else:
            task.modify_task(task_description=form.task.data, task_project=form.project.data,
                             tags=form.tags.data, due_date=form.due_date.data,
                             task_uuid=form.uuid.data)
        return redirect(url_for('tasks'))

    starting_tasks = task.task_list_pending(None)
    return render_template('tasks.html', tasks=starting_tasks, form=form, tab='all-incomplete')


@app.route('/overdue', methods=["GET", "POST"])
@login_required
def overdue():
    if request.args:
        task.mark_task_completed(request.args['task_id'])
    overdue_tasks = task.task_list_overdue()
    return render_template('partials/task_table.html', tasks=overdue_tasks, tab="overdue")


@app.route('/due-today', methods=["GET", "POST"])
@login_required
def due_today():
    """The tasks that have a due date of today."""
    if request.args:
        task.mark_task_completed(request.args['task_id'])
    today = datetime.today()
    today_tasks = task.task_list_pending(today)
    return render_template('partials/task_table.html', tasks=today_tasks, tab="due-today")


@app.route('/due-this-month', methods=["GET", "POST"])
@login_required
def due_this_month():
    if request.args:
        task.mark_task_completed(request.args['task_id'])
    today = datetime.today().astimezone()
    month_tasks = task.task_list_pending(today - timedelta(today.day), today + timedelta(find_end(today, "month")))
    return render_template('partials/task_table.html', tasks=month_tasks, tab='due-this-month')


@app.route('/all-incomplete', methods=["GET", "POST"])
@login_required
def all_incomplete():
    if request.args:
        task.mark_task_completed(request.args['task_id'])
    all_incomplete_tasks = task.task_list_pending(None)
    return render_template('partials/task_table.html', tasks=all_incomplete_tasks, tab='all-incomplete')


@app.route('/completed', methods=["GET", "POST"])
@login_required
def completed():
    if request.args:
        task.mark_task_incomplete(request.args['task_id'])
    completed_tasks = task.task_list_completed()
    return render_template('partials/task_table.html', tasks=completed_tasks, tab='completed')


if __name__ == '__main__':
    app.run()
