import sys
import os
from datetime import datetime

# Add current directory to path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from sqlalchemy.orm import Session
from models import _Session, Usuario, Cliente, Barbeiro, TipoUsuario, Base, engine
from werkzeug.security import generate_password_hash

def seed_users():
    # Garante que as tabelas existam
    print("Verificando/Criando tabelas do banco de dados...")
    Base.metadata.create_all(bind=engine)
    
    session = _Session()
    try:
        print("Iniciando processo de seeding...")
        
        # 1. Criar 20 usuários (inicialmente como clientes)
        users_created_this_run = []
        
        for i in range(1, 21):
            email = f"usuario_teste_{i}@exemplo.com"
            
            # Verifica se já existe
            existing = session.query(Usuario).filter_by(email=email).first()
            if existing:
                print(f"Usuário {email} já existe. Pulando criação.")
                if existing not in users_created_this_run:
                     users_created_this_run.append(existing)
                continue
            
            nome = f"Usuario Teste {i}"
            senha = "senha123" # Senha padrão
            senha_hash = generate_password_hash(senha)
            
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                telefone=f"1199999{i:04d}",
                senha_hash=senha_hash,
                tipo=TipoUsuario.CLIENTE,
                ativo=True
            )
            session.add(novo_usuario)
            session.flush() # Para gerar o ID
            
            # Criar registro de Cliente associado
            novo_cliente = Cliente(id_cliente=novo_usuario.id_usuario)
            session.add(novo_cliente)
            
            users_created_this_run.append(novo_usuario)
            print(f"Usuário criado: {email} (ID: {novo_usuario.id_usuario})")
        
        session.commit()
        print("Criação de usuários finalizada.")
        
        # 2. Realocar 10 usuários como barbeiros
        # Vamos pegar os últimos 10 usuários criados (ou encontrados) para garantir que temos usuários para promover
        # Ou simplesmente pegar 10 usuários do tipo CLIENTE.
        
        # Atualiza a lista de usuários do banco para ter certeza
        candidatos_a_barbeiro = session.query(Usuario).filter(Usuario.tipo == TipoUsuario.CLIENTE).limit(10).all()
        
        if len(candidatos_a_barbeiro) < 10:
             print(f"Aviso: Encontrados apenas {len(candidatos_a_barbeiro)} clientes para promover a barbeiro (esperado: 10).")
        
        print(f"Promovendo {len(candidatos_a_barbeiro)} usuários para a função de Barbeiro...")
        
        for usuario in candidatos_a_barbeiro:
            print(f"Promovendo {usuario.email} para Barbeiro...")
            
            # Atualiza o tipo
            usuario.tipo = TipoUsuario.BARBEIRO
            
            # Verifica se já existe registro de Barbeiro
            barbeiro_existente = session.query(Barbeiro).filter_by(id_barbeiro=usuario.id_usuario).first()
            
            if not barbeiro_existente:
                novo_barbeiro = Barbeiro(
                    id_barbeiro=usuario.id_usuario,
                    especialidade="Corte Clássico",
                    comissao=50.00,
                    ativo=True
                )
                session.add(novo_barbeiro)
            
            # Opcional: Poderíamos remover o registro de Cliente se fosse estritamente necessário,
            # mas vamos manter por segurança de dados, já que o modelo permite.
            
        session.commit()
        print("Realocação concluída com sucesso!")

    except Exception as e:
        session.rollback()
        print(f"Erro durante o seeding: {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    seed_users()
