from taskwarrior import Client

client = Client()


# tasks = client.filter(status="pending")

# for task in tasks:
#    print(task)

def task_list():
    """Return a list of tasks. Will add more features to this eventually for the sake of DRY. """
    tasks = client.filter(status="pending", due="today")
    return tasks
