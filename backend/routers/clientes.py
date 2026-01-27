from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario, Agendamento, Preferencia, TipoUsuario
from schemas import PreferenciaRequest
from dependencies import get_db, get_current_user

router = APIRouter(tags=["Clientes"])

@router.get('/api/clientes')
def listar_clientes(db: Session = Depends(get_db)):
    clientes = db.query(Usuario).filter(Usuario.tipo == TipoUsuario.CLIENTE).all()
    return [{"id": c.id_usuario, "nome": c.nome, "email": c.email} for c in clientes]

@router.get('/api/clientes/agendamentos')
def listar_agendamentos_cliente(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != TipoUsuario.CLIENTE: raise HTTPException(status_code=403, detail="Acesso negado")
    return db.query(Agendamento).filter_by(id_cliente=current_user.id_usuario).all()

@router.get('/api/clientes/preferencias')
def listar_preferencias(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != TipoUsuario.CLIENTE: raise HTTPException(status_code=403, detail="Acesso negado")
    preferencias = db.query(Preferencia).filter_by(id_cliente=current_user.id_usuario).all()
    return [{"id": p.id_preferencia, "descricao": p.descricao} for p in preferencias]

@router.post('/api/clientes/preferencias')
def adicionar_preferencia(data: PreferenciaRequest, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != TipoUsuario.CLIENTE: raise HTTPException(status_code=403, detail="Acesso negado")
    db.add(Preferencia(id_cliente=current_user.id_usuario, descricao=data.descricao))
    db.commit()
    return {"mensagem": "Preferência adicionada"}