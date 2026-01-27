
# Usar uma imagem base leve do Python
FROM python:3.13-slim

# Definir variáveis de ambiente para o Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1

# Adicionar o diretório do Poetry ao PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Instalar dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de definição de dependência
COPY pyproject.toml poetry.lock ./

# Instalar as dependências (sem instalar o próprio projeto ainda)
RUN poetry install --no-root --without dev

# Copiar o restante do código da aplicação
COPY . .

# Expor a porta que a aplicação irá rodar
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
