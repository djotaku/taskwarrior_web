from datetime import datetime

from taskwarrior import Client

client = Client()


def task_list_pending(due_date_start: datetime, due_date_end: datetime | None = None):
    """Return a list of tasks. Will add more features to this eventually for the sake of DRY. """
    tasks = client.filter(status="pending")
    if due_date_start and due_date_end:
        pass
    elif due_date_start:
        filtered_tasks = [task for task in tasks if task.due is not None]  # filter out tasks without due dates
        return [task for task in filtered_tasks if
                task.due.year == due_date_start.year and task.due.month == due_date_start.month and task.due.day == due_date_start.day]
    else:
        return tasks


def task_list_overdue():
    tasks = client.filter(status="pending")
    filtered_tasks = [task for task in tasks if task.due is not None]  # filter out tasks without due dates
    present = datetime.now().astimezone()
    return [task for task in filtered_tasks if task.due < present]
