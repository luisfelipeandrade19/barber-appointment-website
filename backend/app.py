from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import auth, usuarios, barbeiros, clientes, agendamentos, notificacoes, servicos
import uvicorn

app = FastAPI()

# Configura CORS
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handler para garantir que erros retornem {"erro": "mensagem"} mantendo compatibilidade com o frontend
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"erro": exc.detail},
    )

# Incluindo as rotas
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(barbeiros.router)
app.include_router(clientes.router)
app.include_router(agendamentos.router)
app.include_router(notificacoes.router)
app.include_router(servicos.router)

@app.get('/')
def index():
    return {"mensagem": "API Barbearia Online"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)
