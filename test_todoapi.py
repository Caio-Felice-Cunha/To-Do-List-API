"""Tests for the To-Do List API.

Run with: pytest

Each test resets the in-memory list so cases stay independent. The suite
covers the happy path (insert, list, filter, get, modify, delete) and the
edge cases that were bugs in earlier versions: negative ids, out-of-range
ids, an `optional` filter value outside 0-2, and POST /insert without a
deadline.
"""

from fastapi.testclient import TestClient

import todoapi
from todoapi import app

client = TestClient(app)


def setup_function(_func):
    """Empty the shared list before every test."""
    todoapi.todolist.clear()


def _insert(task='buy milk', done=False, deadline=None):
    body = {'task': task, 'done': done}
    if deadline is not None:
        body['deadline'] = deadline
    return client.post('/insert', json=body)


def test_insert_returns_success():
    resp = _insert()
    assert resp.status_code == 200
    assert resp.json() == {'status': 'success'}


def test_insert_without_deadline_is_accepted():
    # Regression: deadline must be optional under Pydantic v2.
    resp = _insert(task='no deadline')
    assert resp.status_code == 200


def test_list_returns_all_items():
    _insert(task='a')
    _insert(task='b')
    resp = client.post('/mylist')
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_list_filter_pending_and_done():
    _insert(task='pending', done=False)
    _insert(task='finished', done=True)

    pending = client.post('/mylist', params={'optional': 1}).json()
    assert [t['task'] for t in pending] == ['pending']

    done = client.post('/mylist', params={'optional': 2}).json()
    assert [t['task'] for t in done] == ['finished']


def test_list_invalid_optional_is_rejected():
    # Regression: optional outside 0-2 used to return 200 with null body.
    _insert()
    resp = client.post('/mylist', params={'optional': 5})
    assert resp.status_code == 422


def test_get_existing_todo():
    _insert(task='first')
    resp = client.get('/todo/0')
    assert resp.status_code == 200
    assert resp.json()['task'] == 'first'


def test_get_negative_id_is_404():
    # Regression: negative index used to leak the last item.
    _insert(task='only')
    resp = client.get('/todo/-1')
    assert resp.status_code == 404


def test_get_out_of_range_id_is_404():
    _insert(task='only')
    resp = client.get('/todo/99')
    assert resp.status_code == 404


def test_modify_status_toggles():
    _insert(task='toggle me', done=False)
    assert client.post('/modifyStatus', params={'id': 0}).status_code == 200
    assert client.get('/todo/0').json()['done'] is True


def test_modify_status_negative_id_is_404():
    _insert(task='only')
    resp = client.post('/modifyStatus', params={'id': -1})
    assert resp.status_code == 404


def test_delete_removes_item():
    _insert(task='delete me')
    assert client.post('/deleteItem', params={'id': 0}).status_code == 200
    assert client.post('/mylist').json() == []


def test_delete_negative_id_is_404():
    # Regression: id=-1 used to silently delete the last item.
    _insert(task='keep me')
    resp = client.post('/deleteItem', params={'id': -1})
    assert resp.status_code == 404
    assert len(client.post('/mylist').json()) == 1
