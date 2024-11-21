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
        return { 'status': 'error'}

@app.post('/mylist')
def mylist(optional: int = 0):
    if optional == 0:
        return todolist
    elif optional == 1:
        return list(filter(lambda x: x.done == False, todolist))

    elif optional == 2:
        return list(filter(lambda x: x.done == True, todolist))

@app.get('/todo/{id}')
def mylist(id: int):
    try:
        return todolist[id]
    except:
        return {'status': f'There is no to-do registered in this id {id}'}

@app.post('/modifyStatus')
def modifyStatus(id: int):
    try:
        todolist[id].done = not todolist[id].done
        return {'status': 'success'}

    except:
        return {'status': 'error'}


@app.post('/deleteItem')
def deleteItem(id: int):
    try:
        del todolist[id]
        return {'status': 'success'}
    except:
        return {'status': 'error'}











