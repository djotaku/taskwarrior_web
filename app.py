from flask import Flask
from flask import render_template
import task

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/due-today')
def due_today():
    """The tasks that have a due date of today."""
    tasks = task.task_list()
    return render_template('due_today.html', tasks=tasks)


if __name__ == '__main__':
    app.run()
