import uuid

# In-memory seed data for the demo API.
tasks = [
    {
    "id":  str(uuid.uuid4()),
    "title": "Learn Flask",
    "completed": False
},
{
    "id":  str(uuid.uuid4()),
    "title": "Build API",
    "completed": False
},
{
    "id":  str(uuid.uuid4()),
    "title": "Test with Postman",
    "completed": True
}]


def get_tasks():
    # Return the full task list as stored in memory.
    return tasks


def get_task(task_id):
    # Find one task by its generated id.
    for task in tasks:
        if task_id == task["id"]:
             return task


def create_task(task_data):
    # New tasks are always created as incomplete.
    new_task = {
    "id": str(uuid.uuid4()),
    "title": task_data["title"].strip(),
    "completed": False
        }
    tasks.append(new_task)