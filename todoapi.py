from xmlrpc.client import boolean
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date

app = FastAPI()

class Todo(BaseModel):
    task: str
    done: boolean
    deadline: Optional[date]

list = []

@app.post('/insert')
def insert(todo: Todo):







