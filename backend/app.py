from flask import Flask, jsonify, request
from flask_cors import CORS
from models import _Session, Servico, Barbeiro, Agendamento
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# Configura CORS para permitir que o frontend (localhost:5173) acesse este backend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Helper para gerenciar a sessão do banco
def get_db_session():
    return _Session()

@app.route('/api/servicos', methods=['GET'])
def listar_servicos():
    session = get_db_session()
    try:
        # Consulta usando o modelo definido em models.py
        servicos = session.query(Servico).filter_by(ativo=True).all()
        
        # Serialização manual para garantir compatibilidade JSON (Decimal -> float)
        resultado = []
        for s in servicos:
            resultado.append({
                "id": s.id_servico,
                "nome": s.nome,
                "descricao": s.descricao,
                "preco": float(s.preco), # JSON não suporta Decimal nativamente
                "duracao_estimada": s.duracao_estimada,
                "id_barbeiro": s.id_barbeiro_criador
            })
            
        return jsonify(resultado)
    except SQLAlchemyError as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

@app.route('/api/barbeiros', methods=['GET'])
def listar_barbeiros():
    session = get_db_session()
    try:
        barbeiros = session.query(Barbeiro).filter_by(ativo=True).all()
        resultado = []
        for b in barbeiros:
            # Precisamos acessar o objeto Usuario relacionado para pegar o nome
            resultado.append({
                "id": b.id_barbeiro,
                "nome": b.usuario.nome if b.usuario else "Desconhecido",
                "especialidade": b.especialidade
            })
        return jsonify(resultado)
    except SQLAlchemyError as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

# Exemplo de rota raiz para teste
@app.route('/')
def index():
    return jsonify({"mensagem": "API Barbearia Online"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
