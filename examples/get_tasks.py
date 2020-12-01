import FireflyAPI

# Replace with your own Authentication Blob
auth_blob = "eyJkZ...UwMSJ9"

# In this example we will try to:
# - Get all the tasks you have left to do

# Lets start by getting your task interface.
user_integration = FireflyAPI.AuthenticatedUser(auth_blob)
task_interface = user_integration.get_task_interface()

# Now let's get all the tasks that you have left to do.

tasks = task_interface.get_tasks()
for task in tasks:
    print(f"{task.title}, due {task.due_date}")

# Now let's get any tasks that you haven't read yet
# We will start by creating a task filter:

task_filter = FireflyAPI.tasks.TaskInterfaceFilter("AllIncludingArchived", read=False, results=50)

# We can pass this filter onto the get tasks method, which will use this filter instead of the default one.
tasks = task_interface.get_tasks(task_filter)
for task in tasks:
    print(f"New events for: {task.title}, set by {task.set_by}")
    # Lets get all the events for the task
    task_events = task.event_store.events
    for event in task_events:
        # We are only interested in the events that we haven't read
        if not event.read:
            print(f"- {type(event)}, {event.createdTime}")

# That should have printed out a list of 'events' that you haven't read (clicked on) yet.
