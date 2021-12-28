from fastapi import APIRouter, Depends
from typing import List

import api.cruds.task as task_crud
import api.schemas.task as task_schema
from api.db import get_db
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

router = APIRouter()
@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
  return await task_crud.get_tasks_with_done(db)

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
  return await task_crud.create_task(db, task_body)

@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int,task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
  task = await task_crud.get_task(db, task_id=task_id)
  if task is None:
    raise HTTPException(status_code=404, detail="Task not found")
  return await task_crud.update_task(db, task_body, original=task)

@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
  task = await task_crud.get_task(db, task_id=task_id)
  if task is None:
    raise HTTPException(status_code=404, detail="Task not found")
  return await task_crud.delete_task(db, original=task)