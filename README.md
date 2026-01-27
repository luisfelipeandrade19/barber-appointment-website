# Barber Appointment Website

Bem-vindo ao repositório do **Barber Appointment Website**. Este projeto é um sistema completo para agendamento de horários em barbearias.

---

## 🚀 Instalação e Execução

O sistema foi projetado para rodar de forma limpa e isolada utilizando **Docker** e **Docker Compose**. Não é necessário instalar Python ou PostgreSQL localmente.

### Pré-requisitos

*   **Docker**
*   **Docker Compose**

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/luisfelipeandrade19/barber-appointment-website.git
    cd barber-appointment-website
    ```

2.  **Suba os containers:**
    Execute o comando abaixo para construir as imagens e iniciar os serviços em segundo plano:
    ```bash
    docker compose up --build -d
    ```

3.  **Verifique o status:**
    ```bash
    docker compose ps
    ```
    Você deverá ver três containers rodando: `barber_backend`, `barber_db` e `barber_frontend`.

4.  **Acesse a aplicação:**
    *   **Frontend**: [http://localhost:5173](http://localhost:5173)
    *   **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

5.  **Populando o Banco de Dados (Opcional):**
    Para criar dados iniciais (usuários e barbeiros), você pode executar o script de seed diretamente dentro do container:
    ```bash
    docker exec -it barber_backend python seed_users.py
    ```

---

## 🛠️ Tecnologias e Dependências

### Frontend
*   **Biblioteca**: React 19
*   **Build Tool**: Vite
*   **Linguagem**: TypeScript
*   **Testes E2E**: Playwright
*   **Roteamento**: React Router DOM 7
*   **Estilização**: CSS Modules / Vanilla CSS
*   **Autenticação Social**: Google & Facebook Login
*   **Linting**: ESLint

### Backend
*   **Linguagem**: Python 3.13
*   **Framework Web**: [FastAPI](https://fastapi.tiangolo.com/) (Alta performance e fácil validação)
*   **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) (Modelagem e interação com banco)
*   **Migrações**: [Alembic](https://alembic.sqlalchemy.org/) (Gerenciamento de schema)
*   **Autenticação**: Python-Jose (JWT) & Passlib/Bcrypt
*   **Gerenciamento de Pacotes**: [Poetry](https://python-poetry.org/)

### Banco de Dados
*   **SGBD**: PostgreSQL 15

### Infraestrutura
*   **Containerização**: Docker
*   **Orquestração**: Docker Compose

---

## 📂 Estrutura do Projeto

A estrutura de diretórios é organizada da seguinte forma:

```
barber-appointment-website/
├── backend/                # Código fonte do Backend (API)
│   ├── alembic/            # Configurações e versões de migração do banco
│   ├── routers/            # Rotas da API (Endpoints) separadas por contexto
│   ├── app.py              # Ponto de entrada da aplicação FastAPI
│   ├── models.py           # Definição dos modelos do banco de dados (ORM)
│   ├── schemas.py          # Schemas Pydantic para validação de dados
│   ├── dependencies.py     # Injeção de dependências (ex: get_db, get_current_user)
│   ├── seed_users.py       # Script para popular o banco com dados de teste
│   ├── Dockerfile          # Definição da imagem Docker do backend
│   ├── pyproject.toml      # Arquivo de configuração e dependências (Poetry)
│   └── .env                # Variáveis de ambiente (não versionado por segurança)
├── frontend/               # Código fonte do Frontend (Aplicação React)
├── docker-compose.yml      # Orquestração dos serviços (App + Banco)
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Documentação do projeto
```

---

## 🐳 Utilizando com Docker

O ambiente é totalmente controlado pelo `docker-compose.yml`, que define três serviços principais:

### 1. `db` (Banco de Dados)
*   **Imagem**: `postgres:15`
*   **Porta Exposta**: `5432` (Acessível localmente)
*   **Persistência**: Utiliza um volume nomeado `postgres_data` para garantir que os dados não sejam perdidos ao reiniciar os containers.

### 2. `backend` (API)
*   **Imagem**: Construída a partir do `backend/Dockerfile`.
*   **Porta Exposta**: `8000`
*   **Dependência**: Aguarda o serviço `db` iniciar antes de subir.

### 3. `frontend` (Aplicação Web)
*   **Imagem**: Construída a partir do `frontend/Dockerfile` (Multi-stage build).
*   **Porta Exposta**: `5173` (Mapeada da porta 80 do container)
*   **Acesso**: [http://localhost:5173](http://localhost:5173)

#### Comandos Úteis

*   **Parar tudo:**
    ```bash
    docker compose down
    ```
*   **Acessar logs do backend:**
    ```bash
    docker compose logs -f backend
    ```
*   **Acessar logs do frontend:**
    ```bash
    docker compose logs -f frontend
    ```
*   **Entrar no shell do container backend:**
    ```bash
    docker exec -it barber_backend bash
    ```
*   **Acessar o banco via CLI:**
    ```bash
    docker exec -it barber_db psql -U postgres -d barbersystem
    ```

---

## 💻 Desenvolvimento Local (Frontend)

Caso queira executar o frontend localmente fora do Docker (para desenvolvimento ágil com HMR):

1.  **Navegue até a pasta do frontend:**
    ```bash
    cd frontend
    ```

2.  **Instale as dependências:**
    ```bash
    npm install
    ```

3.  **Execute em modo de desenvolvimento:**
    ```bash
    npm run dev
    ```
    Acesse em [http://localhost:5173](http://localhost:5173).

### Scripts Disponíveis

No diretório `frontend`, você pode executar:

*   `npm run dev`: Inicia o servidor de desenvolvimento.
*   `npm run build`: Compila o projeto para produção.
*   `npm run preview`: Visualiza o build de produção localmente.
*   `npm run lint`: Executa a verificação de código com ESLint.
*   `npm test`: Roda os testes E2E com Playwright.
*   `npm run test:ui`: Roda os testes com interface visual.

---

## ⚙️ Variáveis de Ambiente

O sistema utiliza variáveis de ambiente para configuração sensível. No ambiente Docker, estas são configuradas automaticamente através do `docker-compose.yml` e, opcionalmente, pelo arquivo `.env` dentro de `backend/`.

As principais variáveis configuradas são:

| Variável | Descrição | Valor Padrão (Docker) |
| :--- | :--- | :--- |
| `POSTGRES_USER` | Usuário do Postgres | `postgres` |
| `POSTGRES_PASSWORD` | Senha do Postgres | `1605` (ou definido no .env) |
| `POSTGRES_DB` | Nome do Banco de Dados | `barbersystem` |
| `DATABASE_URL` | String de conexão SQLAlchemy | `postgresql://postgres:1605@db:5432/barbersystem` |
| `JWT_SECRET_KEY` | Chave secreta para tokens | (Definido no .env ou padrão interno) |
| `JWT_ALGORITHM` | Algoritmo de assinatura | `HS256` |

> ⚠️ **Segurança**: Em ambiente de produção, certifique-se de alterar as senhas e chaves secretas.

---

## ✅ Ambiente Limpo

Este projeto foi configurado para **não depender de nenhuma instalação local** além do Docker.
Ao executar o comando `docker compose up --build`, todo o ambiente necessário (Python, dependências, Banco de Dados) é criado e configurado automaticamente em containers isolados, garantindo consistência e evitando conflitos com sua máquina local.
