from datetime import datetime, timedelta
import pytz
from taskwarrior import Client, Task

client = Client()


def task_list_pending(due_date_start: datetime, due_date_end: datetime | None = None):
    """Return a list of tasks. Will add more features to this eventually for the sake of DRY."""
    tasks = client.filter(status="pending")
    filtered_tasks = [
        task for task in tasks if task.due is not None
    ]  # filter out tasks without due dates
    if due_date_start and due_date_end:
        return [
            task
            for task in filtered_tasks
            if due_date_start <= task.due <= due_date_end
        ]
    elif due_date_start:
        return [
            task
            for task in filtered_tasks
            if task.due.year == due_date_start.year
            and task.due.month == due_date_start.month
            and task.due.day == due_date_start.day
        ]
    else:
        return tasks


def task_list_overdue():
    tasks = client.filter(status="pending")
    filtered_tasks = [
        task for task in tasks if task.due is not None
    ]  # filter out tasks without due dates
    present = datetime.now().astimezone()
    return [task for task in filtered_tasks if task.due < present]


def task_list_completed():
    """Return all completed tasks"""
    return client.filter(status="completed")


def mark_task_completed(task_uuid: str):
    """Mark a task completed"""
    our_task = client.get(uuid=task_uuid)
    our_task.status = "completed"
    client.modify(our_task)


def add_task(task_description: str, task_project: str, tags: str, due_date: datetime):
    tag_list = tags.split()
    print(type(due_date))
    print(due_date)
    timezone = pytz.timezone("America/New_York")
    timezoned_due_date = timezone.localize(due_date)
    # I don't know why, but you can't add in the date as a datetime, but you can modify it afterward.
    new_task = Task(
        description=task_description,
        project=task_project,
        tags=tag_list,
    )
    client.add(new_task)
    new_task.due = timezoned_due_date
    client.modify(new_task)


def mark_task_incomplete(task_uuid: str):
    our_task = client.get(uuid=task_uuid)
    our_task.status = "pending"
    client.modify(our_task)


def get_task(task_uuid: str):
    """Gets a task from taskwarrior.

    Currently only used when getting a task for modification.

    Therefore, changing the timezone to UTC so that it displays correctly on the webpage.
    """
    shift = timedelta(hours=-5)
    task = client.get(uuid=task_uuid)
    task.due = task.due + shift
    return task


def modify_task(
    task_description: str,
    task_project: str,
    tags: str,
    due_date: datetime,
    task_uuid: str,
):
    tag_list = tags.split()
    task_to_modify = client.get(task_uuid)
    timezone = pytz.timezone("America/New_York")
    timezoned_due_date = timezone.localize(due_date)
    task_to_modify.description = task_description
    task_to_modify.project = task_project
    task_to_modify.tags = tag_list
    task_to_modify.due = timezoned_due_date
    client.modify(task_to_modify)
