from datetime import datetime, timedelta, timezone
from taskchampion import Replica, Status, Operations, Tag
import uuid

replica = Replica.new_on_disk("/root/.task/", False)


def task_list_pending(due_date_start: datetime, due_date_end: datetime | None = None):
    """Return a list of tasks. Will add more features to this eventually for the sake of DRY."""
    tasks = []
    task_dict = replica.all_tasks()
    for uuid in task_dict.keys():
        task = replica.get_task(uuid)
        if task.get_status () == Status.Pending:
            tasks.append(task)
    filtered_tasks = [
        task for task in tasks if task.get_due() is not None
    ]  # filter out tasks without due dates
    if due_date_start and due_date_end:
        return [
            task
            for task in filtered_tasks
            if due_date_start <= task.get_due() <= due_date_end
        ]
    elif due_date_start:
        return [
            task
            for task in filtered_tasks
            if task.get_due().year == due_date_start.year
            and task.get_due().month == due_date_start.month
            and task.get_due().day == due_date_start.day
        ]
    else:
        return tasks


def task_list_overdue():
    tasks = []
    task_dict = replica.all_tasks()
    for uuid in task_dict.keys():
        task = replica.get_task(uuid)
        if task.get_status () == Status.Pending:
            tasks.append(task)
    filtered_tasks = [
        task for task in tasks if task.get_due() is not None
    ]  # filter out tasks without due dates 
    present = datetime.now().astimezone()
    return [task for task in filtered_tasks if task.get_due() < present]


def task_list_completed():
    """Return all completed tasks"""
    tasks = []
    task_dict = replica.all_tasks()
    for uuid in task_dict.keys():
        task = replica.get_task(uuid)
        if task.get_status () == Status.Completed:
            tasks.append(task)
    return tasks 


def mark_task_completed(task_uuid: str):
    """Mark a task completed"""
    our_task = replica.get_task(task_uuid)
    operations = Operations()
    our_task.set_status(Status.Completed, operations)
    replica.commit_operations(operations)


def add_task(task_description: str, task_project: str, tags: str, due_date: datetime):
    tag_list = tags.split()
    operations = Operations()
    task_uuid = str(uuid.uuid4())
    task = replica.create_task(task_uuid, operations)
    task.set_description(task_description, operations)
    task.set_entry(datetime.now(timezone.utc), operations)
    task.set_value("project", task_project, operations)
    task.set_status(Status.Pending, operations)
    for tag in tag_list:
        this_tag = Tag(tag)
        task.add_tag(this_tag, operations)
    replica.commit_operations(operations)


def mark_task_incomplete(task_uuid: str):
    our_task = replica.get_task(task_uuid)
    operations = Operations()
    our_task.set_status(Status.Pending, operations)
    replica.commit_operations(operations)


def get_task(task_uuid: str):
    """Gets a task from taskwarrior.

    Currently only used when getting a task for modification.
    """
    return replica.get_task(task_uuid)


def modify_task(
    task_description: str,
    task_project: str,
    tags: str,
    due_date: datetime,
    task_uuid: str,
):
    operations = Operations()
    tag_list = tags.split()
    task_to_modify = replica.get_task(task_uuid)
    task_to_modify.set_description(task_description, operations)
    task_to_modify.set_entry(due_date.astimezone(), operations)
    task_to_modify.set_value("project", task_project, operations)
    for tag in tag_list:
        this_tag = Tag(tag)
        task_to_modify.add_tag(this_tag, operations)
    replica.commit_operations(operations)