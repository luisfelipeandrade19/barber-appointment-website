from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from models import Usuario, Barbeiro, TipoUsuario, Servico, DisponibilidadeBarbeiro, TipoDisponibilidade
from schemas import BarbeiroCreateRequest, UpdatePerfilRequest
from dependencies import get_db, get_current_user
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, time, date

router = APIRouter(tags=["Usuarios"])

@router.post('/api/admin/barbeiros', status_code=status.HTTP_201_CREATED)
def criar_barbeiro(data: BarbeiroCreateRequest, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != TipoUsuario.ADMIN and current_user.tipo != 'admin':
        raise HTTPException(status_code=403, detail="Acesso negado")

    if db.query(Usuario).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email já registrado")

    try:
        # 1. Criar Usuario
        novo_usuario = Usuario(
            nome=data.nome,
            email=data.email,
            telefone=data.telefone,
            senha_hash=generate_password_hash(data.senha),
            tipo=TipoUsuario.BARBEIRO
        )
        db.add(novo_usuario)
        db.flush()

        # 2. Criar Barbeiro
        novo_barbeiro = Barbeiro(
            id_barbeiro=novo_usuario.id_usuario,
            especialidade=data.especialidade or "Geral",
            ativo=True
        )
        db.add(novo_barbeiro)
        db.flush() # Para garantir que o ID do barbeiro esteja disponivel (é o mesmo do usuario)

        # 3. Criar Serviços Fixos
        servicos_fixos = [
            {"nome": "Corte de Cabelo", "preco": 30.00, "duracao": 30},
            {"nome": "Barba", "preco": 20.00, "duracao": 20},
            {"nome": "Barba + Cabelo", "preco": 45.00, "duracao": 50}
        ]
        
        for sv in servicos_fixos:
            db.add(Servico(
                nome=sv["nome"],
                descricao="Serviço padrão",
                preco=sv["preco"],
                duracao_estimada=sv["duracao"],
                id_barbeiro_criador=novo_barbeiro.id_barbeiro,
                ativo=True
            ))



        # 5. Criar Disponibilidade (Próximos 60 dias)
        hoje = date.today()
        for i in range(60):
            dia_atual = hoje + timedelta(days=i)
            for h in range(9, 19):
                hora_inicio = time(hour=h, minute=0)
                hora_fim = time(hour=h+1, minute=0)
                
                db.add(DisponibilidadeBarbeiro(
                    id_barbeiro=novo_barbeiro.id_barbeiro,
                    data=dia_atual,
                    hora_inicio=hora_inicio,
                    hora_fim=hora_fim,
                    tipo=TipoDisponibilidade.DISPONIVEL,
                    recorrente=False # Gerando explicitamente
                ))

        db.commit()
        return {"mensagem": "Barbeiro criado com sucesso com serviços e agenda padrão"}
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
    if data.telefone: current_user.telefone = data.telefone
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