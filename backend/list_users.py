from models import _Session, Usuario

def listar_usuarios():
    db = _Session()
    try:
        usuarios = db.query(Usuario).all()
        print("-" * 50)
        print(f"{'ID':<5} | {'NOME':<20} | {'EMAIL':<25}")
        print("-" * 50)
        for u in usuarios:
            print(f"{u.id_usuario:<5} | {u.nome:<20} | {u.email:<25}")
        print("-" * 50)
    except Exception as e:
        print(f"Erro ao listar: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    listar_usuarios()
