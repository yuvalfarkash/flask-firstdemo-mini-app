from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity
from bson.objectid import ObjectId 
from models import tasks 
from db import db

tasks_bp = Blueprint("tasks", __name__)

tasks_col = db.todo

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    
    all_tasks = []
    for task in tasks_col.find():
        task["_id"] = str(task["_id"])
        all_tasks.append(task)
    return jsonify(all_tasks)


@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    try:
        task = tasks_col.find_one({"_id": ObjectId(task_id)})
        if task:
            task["_id"] = str(task["_id"])
            return jsonify(task)
    except:
        pass 
        
    raise NotFound(f"{task_id} not found")


@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        raise BadRequest("request body must be json")
    if "title" not in data:
        raise BadRequest("title is required")
    title = data["title"]
    if not isinstance(title, str):
        raise BadRequest("title must be a string")
    if not title.strip():
        raise UnprocessableEntity("title must contain text")

    new_task = {
        "title": title.strip(),
        "completed": False  
    }
    
    tasks_col.insert_one(new_task)
    
    new_task["_id"] = str(new_task["_id"])
    
    return jsonify({
        "success": True,
        "data": new_task
    }), 201


@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def change_task(task_id):
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        raise BadRequest("error: update request must contain data")
    
    allowed_keys = ("title", "completed")
    update_data = {}

    for key, value in data.items():
        if key not in allowed_keys:
            raise BadRequest(f"not allowed to pass {key}")
        
        if key == "title":
            if not isinstance(value, str) or not value.strip():
                raise BadRequest("title must be a non-empty string")
            update_data["title"] = value.strip()
        
        if key == "completed":
            if not isinstance(value, bool):
                raise BadRequest("completed must be a boolean")
            update_data["completed"] = value

    try:
        result = tasks_col.update_one(
            {"_id": ObjectId(task_id)}, 
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise NotFound(f"{task_id} not found")
            
        updated_task = tasks_col.find_one({"_id": ObjectId(task_id)})
        updated_task["_id"] = str(updated_task["_id"])
        return jsonify(updated_task)
    except:
        raise NotFound(f"{task_id} not found")


@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        result = tasks_col.delete_one({"_id": ObjectId(task_id)})
        
        if result.deleted_count == 0:
            raise NotFound(f"{task_id} not found")

        return jsonify({
            "success": True,
            "message": f"removed task {task_id}"
        })
    except:
        raise NotFound(f"{task_id} not found")