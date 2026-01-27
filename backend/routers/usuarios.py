from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from models import Usuario, Barbeiro, TipoUsuario
from schemas import BarbeiroCreateRequest, UpdatePerfilRequest
from dependencies import get_db, get_current_user
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(tags=["Usuarios"])

@router.post('/api/admin/barbeiros', status_code=status.HTTP_201_CREATED)
def criar_barbeiro(data: BarbeiroCreateRequest, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != TipoUsuario.ADMIN and current_user.tipo != 'admin':
        raise HTTPException(status_code=403, detail="Acesso negado")

    if db.query(Usuario).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email já registrado")

    try:
        novo_usuario = Usuario(
            nome=data.nome,
            email=data.email,
            senha_hash=generate_password_hash(data.senha),
            tipo=TipoUsuario.BARBEIRO
        )
        db.add(novo_usuario)
        db.flush()

        novo_barbeiro = Barbeiro(
            id_barbeiro=novo_usuario.id_usuario,
            especialidade=data.especialidade,
            ativo=True
        )
        db.add(novo_barbeiro)
        db.commit()
        return {"mensagem": "Barbeiro criado com sucesso"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/api/usuarios')
def listar_usuarios(skip: int = 0, limit: int = 100, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return [{"id": u.id_usuario, "nome": u.nome, "email": u.email, "tipo": u.tipo.value, "ativo": getattr(u, 'ativo', True)} for u in usuarios]

@router.delete('/api/usuarios/{id_usuario}')
def deletar_usuario(id_usuario: int, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id_usuario != id_usuario and current_user.tipo != TipoUsuario.ADMIN:
        raise HTTPException(status_code=403, detail="Acesso negado")
        
    usuario = db.query(Usuario).get(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    
    usuario.ativo = False
    db.commit()
    return {"mensagem": "Usuario desativado com sucesso"}
@router.put('/api/perfil')
def atualizar_perfil(data: UpdatePerfilRequest, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.nome: current_user.nome = data.nome
    db.commit()
    return {"mensagem": "Perfil atualizado"}

@router.get('/api/perfil')
def obter_perfil(current_user: Usuario = Depends(get_current_user)):
    data = {
        "id": current_user.id_usuario, 
        "nome": current_user.nome, 
        "email": current_user.email, 
        "tipo": current_user.tipo.value,
        "telefone": current_user.telefone,
        "data_cadastro": current_user.data_cadastro.isoformat() if current_user.data_cadastro else None
    }
    
    if current_user.tipo == TipoUsuario.CLIENTE and current_user.cliente:
        data["preferencias"] = current_user.cliente.preferencias
        
    return data