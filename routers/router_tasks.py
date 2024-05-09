from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from classes.schema_dto import Task, TaskNoID

router = APIRouter(
    prefix='/tasks',
    tags=["Tasks"]
)

tasks = [
    Task(id="task1", title="medical appointment", owner="Cylia", completed=True),
    Task(id="task2", title="make call", owner="Cylia", completed=False),
    Task(id="task3", title="send email to client", owner="Cylia", completed=False)
]

@router.get('/', response_model=List[Task])
async def get_tasks():
    return tasks

@router.post('/', response_model=Task, status_code=201)
async def create_task(task_data: TaskNoID):
    generated_id = str(uuid.uuid4())
    new_task = Task(id=generated_id, **task_data.dict())
    tasks.append(new_task)
    return new_task

@router.get('/{task_id}', response_model=Task)
async def get_task_by_id(task_id: str):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.patch('/{task_id}', response_model=Task)
async def modify_task(task_id: str, task_data: TaskNoID):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task_data = task.dict()
            updated_task_data.update(**task_data.dict(exclude_unset=True))
            tasks[index] = Task(**updated_task_data)
            return tasks[index]
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete('/{task_id}', status_code=204)
async def delete_task(task_id: str):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[index]
            return
    raise HTTPException(status_code=404, detail="Task not found")
