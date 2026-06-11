from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date

app = FastAPI()


class Todo(BaseModel):
    task: str
    done: bool
    deadline: Optional[date] = None


todolist = []


def _check_id(id: int):
    """Reject negative and out-of-range ids before indexing the list.

    Python negative indexing would otherwise let id=-1 silently hit the
    last element on get/modify/delete.
    """
    if id < 0 or id >= len(todolist):
        raise HTTPException(
            status_code=404,
            detail=f'There is no to-do registered in this id {id}',
        )


@app.post('/insert')
def insert(todo: Todo):
    todolist.append(todo)
    return {'status': 'success'}


@app.post('/mylist')
def mylist(optional: int = 0):
    if optional == 0:
        return todolist
    elif optional == 1:
        return list(filter(lambda x: not x.done, todolist))
    elif optional == 2:
        return list(filter(lambda x: x.done, todolist))
    raise HTTPException(
        status_code=422,
        detail='optional must be 0 (all), 1 (pending) or 2 (done)',
    )


@app.get('/todo/{id}')
def get_todo(id: int):
    _check_id(id)
    return todolist[id]


@app.post('/modifyStatus')
def modifyStatus(id: int):
    _check_id(id)
    todolist[id].done = not todolist[id].done
    return {'status': 'success'}


@app.post('/deleteItem')
def deleteItem(id: int):
    _check_id(id)
    del todolist[id]
    return {'status': 'success'}
