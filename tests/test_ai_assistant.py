import sys
import os
import pytest
from unittest.mock import patch, MagicMock
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

@patch("app.routes.ai_assistant.genai.GenerativeModel")
def test_get_task_advice(mock_model):
    # Cria uma tarefa para ser analisada
    res = client.post("/tasks/", json={
        "title": "Estudar para prova",
        "description": "Preciso revisar os tópicos de matemática"
    })
    task_id = res.json()["id"]

    # Mocka a resposta da IA
    mock_instance = MagicMock()
    mock_instance.generate_content.return_value.text = "1. Revise os tópicos principais\n2. Faça exercícios"
    mock_model.return_value = mock_instance

    # Chama o endpoint
    response = client.get(f"/ai/advice/{task_id}")
    assert response.status_code == 200
    assert "advice" in response.json()

@patch("app.routes.ai_assistant.genai.GenerativeModel")
def test_process_text_creates_tasks(mock_model):
    # Mocka o retorno da IA com um JSON válido
    mock_instance = MagicMock()
    mock_instance.generate_content.return_value.text = """
    [
        {
            "title": "Fazer compras",
            "description": "Comprar arroz, feijão e carne no mercado"
        },
        {
            "title": "Estudar programação",
            "description": "Praticar FastAPI e testar endpoints"
        }
    ]
    """
    mock_model.return_value = mock_instance

    # Chama o endpoint
    response = client.post("/ai/process-text", json={"text": "Preciso fazer compras e estudar programação"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "Fazer compras"
    assert data[1]["title"] == "Estudar programação"

def test_process_text_returns_500_on_invalid_json():
    # Simula erro quando a IA não retorna um JSON
    with patch("app.routes.ai_assistant.genai.GenerativeModel") as mock_model:
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value.text = "Não encontrei nenhuma tarefa."
        mock_model.return_value = mock_instance

        response = client.post("/ai/process-text", json={"text": "blá blá blá"})
        assert response.status_code == 500
        assert "IA não retornou uma lista JSON válida" in response.text
