from xmlrpc.client import boolean
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date

app = FastAPI()

class Todo(BaseModel):
    task: str
    done: bool
    deadline: Optional[date]

list = []

@app.post('/insert')
def insert(todo: Todo):
    try:
        list.append(todo)
        return {'status': 'success'}
    
    except:
        return { 'status': 'erro'}


@app.post('/list')
def list(optional: int = 0):
    if optional == 0:
        return list
    elif optional == 1:
        return list(filter(lambda x: x.done == False, list))

    elif optional == 2:
        return list(filter(lambda x: x.done == True, list))

    


