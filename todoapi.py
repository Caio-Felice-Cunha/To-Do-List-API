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

todolist = []

@app.post('/insert')
def insert(todo: Todo):
    try:
        todolist.append(todo)
        return {'status': 'success'}
    
    except:
        return { 'status': 'erro'}


@app.post('/mylist')
def mylist(optional: int = 0):
    if optional == 0:
        return todolist
    elif optional == 1:
        return list(filter(lambda x: x.done == False, todolist))

    elif optional == 2:
        return list(filter(lambda x: x.done == True, todolist))

    


