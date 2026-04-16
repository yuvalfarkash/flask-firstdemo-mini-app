from flask import Flask, jsonify, request
from datetime import datetime, timezone
from werkzeug.exceptions import NotFound, BadRequest
import uuid
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "api is running"
    })

tasks = [
    {
        "id": "1",
        "title": "learn flask",
        "completed": False
    },
    {
        "id": "2",
        "title": "Build api",
        "completed": False
    },
    {
        "id": "3",
        "title": "Test with postmen",
        "completed": True
    }
    ]  
@app.route("/tasks")
def get_all_tasks():
    return jsonify(tasks)

@app.route("/tasks/<task_id>")
def checking_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task)
    return jsonify({
        "error": "sorry didnt found"
    }), 404


@app.route("/tasks", methods=['POST'])
def create_task():
    data = request.get_json()
    try:
        if not isinstance(data.get("completed",False), bool):
            return jsonify({
                "error": "sorry completed must be boolean"
            }),400
        new_task ={
            "id": str(uuid.uuid4()),
            "title": data["title"],
            "completed": data.get("completed",False)
        }
        tasks.append(new_task)
        return jsonify(new_task) ,201
    except KeyError:
        return jsonify({
            "error": "missing field",
            "message": " the title field is missing"
        }),400
        
@app.route("/tasks/<task_id>", methods=['PUT'])
def changing_task(task_id):
    new_task = {}
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "sorry u didnt send anything"
        }),400
    for task in tasks:
        if task_id == task["id"]:
            if "title" in data:
                task["title"]= data["title"]
            if "completed" in data:
                if isinstance(data["completed"], bool):
                    task["completed"]= data["completed"]
                else:
                    return jsonify({
                        "error": "sorry completed is not boolean"
                    }),400
            new_task = task
            return jsonify(new_task),200
    return jsonify({   
        "error" : "not found"
        }), 404
    


@app.route("/tasks/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    new_task={}
 
    for task in tasks:
        if task_id == task["id"]:
            new_task=task
            tasks.remove(task)
            return jsonify({
                "seccess": "tasks deleted"   
                }), 200 
    if new_task=={}:
        return jsonify({
            "error": "sorry somthing went wrong"
        }),404
    
    


if __name__ == "__main__":
    app.run(debug=True)   
