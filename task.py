from datetime import datetime

from taskwarrior import Client, Task

client = Client()


def task_list_pending(due_date_start: datetime, due_date_end: datetime | None = None):
    """Return a list of tasks. Will add more features to this eventually for the sake of DRY. """
    tasks = client.filter(status="pending")
    filtered_tasks = [task for task in tasks if task.due is not None]  # filter out tasks without due dates
    if due_date_start and due_date_end:
        return [task for task in filtered_tasks if due_date_start <= task.due <= due_date_end]
    elif due_date_start:
        return [task for task in filtered_tasks if
                task.due.year == due_date_start.year and task.due.month == due_date_start.month and task.due.day == due_date_start.day]
    else:
        return tasks


def task_list_overdue():
    tasks = client.filter(status="pending")
    filtered_tasks = [task for task in tasks if task.due is not None]  # filter out tasks without due dates
    present = datetime.now().astimezone()
    return [task for task in filtered_tasks if task.due < present]


def task_list_completed():
    """Return all completed tasks"""
    tasks = client.filter(status="completed")
    return tasks


def mark_task_completed(task_uuid: str):
    """Mark a task completed"""
    our_task = client.get(uuid=task_uuid)
    our_task.status = "completed"
    client.modify(our_task)


def add_task(task_description: str, task_project: str, tags: str, due_date: datetime):
    print("Now I'm in the function")
    print(type(due_date))
    tag_list = tags.split()
    new_task = Task(description=task_description, project=task_project, tags=tag_list, due=due_date)
    client.add(new_task)
