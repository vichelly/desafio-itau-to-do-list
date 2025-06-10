# Desafio Itaú To-Do List

Projeto simples de API REST para gerenciamento de tarefas, usando FastAPI, SQLAlchemy e PostgreSQL (via Docker).

---

## Pré-requisitos

- Python 3.10+ instalado
- Docker instalado
- Git (opcional, para clonar o projeto)

---

## Passo a passo para rodar o projeto

### 1. Clone o repositório (opcional)

```bash
git clone <url-do-repo>
cd desafio-itau-to-do-list
```

## 2. Criar e ativar ambiente virtual (venv)

No Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
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