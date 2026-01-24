from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario, Cliente, TipoUsuario
from schemas import RegisterRequest, LoginRequest, Token
from dependencies import get_db, create_access_token, create_refresh_token
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(tags=["Autenticação"])

@router.post('/api/register', status_code=status.HTTP_201_CREATED, response_model=Token)
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

        # Gera tokens
        access_token = create_access_token(data={"sub": novo_usuario.email, "tipo": novo_usuario.tipo.value})
        refresh_token = create_refresh_token(data={"sub": novo_usuario.email})

        db.commit()
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "usuario": {
                "id": novo_usuario.id_usuario,
                "nome": novo_usuario.nome,
                "tipo": novo_usuario.tipo.value
            }
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/api/login', response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(email=data.email).first()

    if usuario and check_password_hash(usuario.senha_hash, data.senha):
        access_token = create_access_token(data={"sub": usuario.email, "tipo": usuario.tipo.value})
        refresh_token = create_refresh_token(data={"sub": usuario.email})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "usuario": {"id": usuario.id_usuario, "nome": usuario.nome, "tipo": usuario.tipo.value}
        }
    raise HTTPException(status_code=401, detail="Credenciais inválidas")