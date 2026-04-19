import uuid


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
    
    return tasks


def get_task(task_id):
    for task in tasks:
        if task_id == task["id"]:
             return task


def create_task(task_data):
    new_task = {
    "id": str(uuid.uuid4()),
    "title": task_data["title"].strip(),
    "completed": False
        }
    tasks.append(new_task)