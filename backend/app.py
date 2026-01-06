from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from models import _Session, Servico, Barbeiro, Agendamento, Usuario, Cliente, TipoUsuario, AgendamentoServico
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
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

# Helper para gerenciar a sessão do banco
def get_db():
    db = _Session()
    try:
        yield db
    finally:
        db.close()

# Pydantic Models
class RegisterRequest(BaseModel):
    nome: str
    email: str
    senha: str
    confirmar_senha: str

class LoginRequest(BaseModel):
    email: str
    senha: str

class AgendamentoRequest(BaseModel):
    id_cliente: int
    id_barbeiro: int
    servicos: List[int]
    data_hora: str

@app.get('/api/servicos')
def listar_servicos(db: Session = Depends(get_db)):
    try:
        servicos = db.query(Servico).filter_by(ativo=True).all()
        
        resultado = []
        for s in servicos:
            resultado.append({
                "id": s.id_servico,
                "nome": s.nome,
                "descricao": s.descricao,
                "preco": float(s.preco),
                "duracao_estimada": s.duracao_estimada,
                "id_barbeiro": s.id_barbeiro_criador
            })
            
        return resultado
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/barbeiros')
def listar_barbeiros(db: Session = Depends(get_db)):
    try:
        barbeiros = db.query(Barbeiro).filter_by(ativo=True).all()
        resultado = []
        for b in barbeiros:
            resultado.append({
                "id": b.id_barbeiro,
                "nome": b.usuario.nome if b.usuario else "Desconhecido",
                "especialidade": b.especialidade
            })
        return resultado
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/register', status_code=status.HTTP_201_CREATED)
def registrar_usuario(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        if data.senha != data.confirmar_senha:
             raise HTTPException(status_code=400, detail="Senhas não conferem")

        if db.query(Usuario).filter_by(email=data.email).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado")

        novo_usuario = Usuario(
            nome=data.nome,
            email=data.email,
            senha_hash=generate_password_hash(data.senha),
            tipo=TipoUsuario.CLIENTE
        )
        db.add(novo_usuario)
        db.flush()

        novo_cliente = Cliente(id_cliente=novo_usuario.id_usuario)
        db.add(novo_cliente)

        db.commit()
        return {"mensagem": "Usuário criado com sucesso"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/login')
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter_by(email=data.email).first()

        if usuario and check_password_hash(usuario.senha_hash, data.senha):
            return {
                "mensagem": "Login realizado com sucesso",
                "usuario": {
                    "id": usuario.id_usuario,
                    "nome": usuario.nome,
                    "tipo": usuario.tipo.value
                }
            }
        else:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/agendamentos', status_code=status.HTTP_201_CREATED)
def criar_agendamento(data: AgendamentoRequest, db: Session = Depends(get_db)):
    try:
        try:
            data_inicio = datetime.fromisoformat(data.data_hora)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido. Use o formato ISO 8601.")
        
        servicos_db = db.query(Servico).filter(Servico.id_servico.in_(data.servicos)).all()
        
        duracao_total = sum([s.duracao_estimada for s in servicos_db])
        valor_total = sum([s.preco for s in servicos_db])
        data_fim = data_inicio + timedelta(minutes=duracao_total)

        novo_agendamento = Agendamento(
            id_cliente=data.id_cliente,
            id_barbeiro=data.id_barbeiro,
            data_hora_inicio=data_inicio,
            data_hora_fim=data_fim,
            tempo_total_estimado=duracao_total,
            valor_total=valor_total
        )
        db.add(novo_agendamento)
        db.flush()

        for servico in servicos_db:
            novo_item = AgendamentoServico(
                id_agendamento=novo_agendamento.id_agendamento,
                id_servico=servico.id_servico,
                preco_na_epoca=servico.preco
            )
            db.add(novo_item)

        db.commit()

        return {"mensagem": "Agendamento realizado com sucesso!"}
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/')
def index():
    return {"mensagem": "API Barbearia Online"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)
