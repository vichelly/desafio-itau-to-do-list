import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ajusta o path para encontrar o módulo 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Limpa e cria as tabelas antes e depois de cada teste
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_task():
    response = client.post("/tasks/", json={"title": "Test task", "description": "desc", "status": "pendente"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert data["status"] == "pendente"
    assert "id" in data

def test_read_all_tasks():
    client.post("/tasks/", json={"title": "T1", "description": "d1", "status": "pendente"})
    client.post("/tasks/", json={"title": "T2", "description": "d2", "status": "concluido"})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_read_one_task():
    res = client.post("/tasks/", json={"title": "T1", "description": "d1", "status": "pendente"})
    task_id = res.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id

def test_update_task():
    res = client.post("/tasks/", json={"title": "Old", "description": "old", "status": "pendente"})
    task_id = res.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "New", "description": "new", "status": "concluido"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New"
    assert data["status"] == "concluido"

def test_delete_task():
    res = client.post("/tasks/", json={"title": "ToDelete", "description": "desc", "status": "pendente"})
    task_id = res.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

    # Verifica que a task foi deletada
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_update_status():
    res = client.post("/tasks/", json={"title": "ToUpdateStatus", "description": "desc", "status": "pendente"})
    task_id = res.json()["id"]

    response = client.patch(f"/tasks/{task_id}/status", json={"status": "concluido"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "concluido"
