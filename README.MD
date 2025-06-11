# Desafio Itaú To-Do List

Projeto simples de API REST para gerenciamento de tarefas, usando FastAPI, SQLAlchemy e PostgreSQL (via Docker).

---

## Pré-requisitos

- Python instalado
- Docker instalado
- Git (opcional, para clonar o projeto)

---

## Passo a passo para rodar o projeto

### 1. Clone o repositório (opcional)

```bash
git clone https://github.com/vichelly/desafio-itau-to-do-list.git
cd desafio-itau-to-do-list
```

## 2. Criar e ativar ambiente virtual (venv)

No Windows PowerShell:

para criar a venv
```bash
py -m venv venv
```

ativar o venv
```bash
.\venv\Scripts\Activate.ps1
```
ou
```bash
source venv/bin/activate
```
## 3. Instalar dependências

Com o ambiente virtual ativado:
```bash
pip install -r requirements.txt
```

## 4. Rodar o banco de dados PostgreSQL com Docker

No terminal, dentro da pasta do projeto, rode:

```bash
docker-compose up -d
```

## 5. Configurar variáveis de ambiente
Crie um arquivo .env na raiz do projeto, com a variável:

```bash
DATABASE_URL=postgresql://"seu db user":"sua senha"@localhost:5432/todo_db
GEMINI_API_KEY=chave da api gemini 
DB_USER=seu db user
DB_PASSWORD=sua senha 
```

ou mude a variável como quiser, altere também no docker compose


## 6. Rodar aplicação

```bash
uvicorn app.main:app --reload
```

## Testar API

testes unitários com pytest
```bash
pytest tests/
```

Você pode testar os endpoints usando o Swagger UI:

http://127.0.0.1:8000/docs


## Parar banco 

```bash
docker-compose down
```

