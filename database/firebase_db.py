import firebase_admin
from firebase_admin import credentials
import pyrebase
from configs.firebase_config_example import firebaseConfig

# Initialisation de Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("../configs/todolist-ab703-firebase-adminsdk-g0omu-1421a4760d.json")
    firebase_admin.initialize_app(cred)

# Initialisation de Pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
authSession = firebase.auth()

def get_all_tasks():
    tasks = db.child("todos").get()
    return [task.val() for task in tasks.each()] if tasks.each() else []

def add_task(task_data):
    result = db.child("todos").push(task_data)
    task_data['id'] = result['name']
    return task_data

def get_task(task_id):
    task = db.child("todos").child(task_id).get()
    if task.val():
        return {**task.val(), "id": task.key()}
    return None

def update_task(task_id, task_data):
    db.child("todos").child(task_id).update(task_data)
    return {**task_data, "id": task_id}

def delete_task(task_id):
    db.child("todos").child(task_id).remove()
