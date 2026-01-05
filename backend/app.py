from flask import Flask, jsonify, request
from flask_cors import CORS
from models import _Session, Servico, Barbeiro, Agendamento, Usuario, Cliente, TipoUsuario, AgendamentoServico
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)

# Configura CORS para permitir que o frontend (localhost:5173) acesse este backend
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

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

@app.route('/api/register', methods=['POST'])
def registrar_usuario():
    session = get_db_session()
    data = request.get_json()

    try:
        # Validação básica
        if not data or not data.get('email') or not data.get('senha') or not data.get('nome'):
             return jsonify({"erro": "Dados incompletos"}), 400

        if data.get('senha') != data.get('confirmar_senha'):
             return jsonify({"erro": "Senhas não conferem"}), 400

        # Verificar se usuário já existe
        if session.query(Usuario).filter_by(email=data.get('email')).first():
            return jsonify({"erro": "Email já cadastrado"}), 400

        # Criar Usuário
        novo_usuario = Usuario(
            nome=data.get('nome'),
            email=data.get('email'),
            senha_hash=generate_password_hash(data.get('senha')),
            tipo=TipoUsuario.CLIENTE # Por padrão, registra como cliente
        )
        session.add(novo_usuario)
        session.flush() # Para gerar o ID do usuário antes de criar o cliente

        # Criar Cliente vinculado
        novo_cliente = Cliente(id_cliente=novo_usuario.id_usuario)
        session.add(novo_cliente)

        session.commit()
        return jsonify({"mensagem": "Usuário criado com sucesso"}), 201

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

@app.route('/api/login', methods=['POST'])
def login():
    session = get_db_session()
    data = request.get_json()

    try:
        email = data.get('email')
        senha = data.get('senha')

        usuario = session.query(Usuario).filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha_hash, senha):
            # Em um app real, aqui você geraria um Token JWT.
            # Para este protótipo, retornamos o ID e o Tipo para o frontend salvar.
            return jsonify({
                "mensagem": "Login realizado com sucesso",
                "usuario": {
                    "id": usuario.id_usuario,
                    "nome": usuario.nome,
                    "tipo": usuario.tipo.value
                }
            }), 200
        else:
            return jsonify({"erro": "Credenciais inválidas"}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

@app.route('/api/agendamentos', methods=['POST'])
def criar_agendamento():
    session = get_db_session()
    data = request.get_json()

    try:
        # Dados esperados: id_cliente, id_barbeiro, servicos (lista de IDs), data_hora (ISO string)
        # Exemplo data_hora: "2023-10-25T14:30:00"
        
        data_inicio = datetime.fromisoformat(data.get('data_hora'))
        
        # Calcular duração total e preço total
        servicos_ids = data.get('servicos', [])
        servicos_db = session.query(Servico).filter(Servico.id_servico.in_(servicos_ids)).all()
        
        duracao_total = sum([s.duracao_estimada for s in servicos_db])
        valor_total = sum([s.preco for s in servicos_db])
        data_fim = data_inicio + timedelta(minutes=duracao_total)

        novo_agendamento = Agendamento(
            id_cliente=data.get('id_cliente'),
            id_barbeiro=data.get('id_barbeiro'),
            data_hora_inicio=data_inicio,
            data_hora_fim=data_fim,
            tempo_total_estimado=duracao_total,
            valor_total=valor_total
        )
        session.add(novo_agendamento)
        session.flush() # Garante que o ID do agendamento seja gerado antes de salvar os serviços

        # Salva a relação de quais serviços foram escolhidos para este agendamento
        for servico in servicos_db:
            novo_item = AgendamentoServico(
                id_agendamento=novo_agendamento.id_agendamento,
                id_servico=servico.id_servico,
                preco_na_epoca=servico.preco # Importante para histórico financeiro se o preço mudar depois
            )
            session.add(novo_item)

        session.commit() # Confirma tudo (Agendamento + Itens)

        return jsonify({"mensagem": "Agendamento realizado com sucesso!"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

# Exemplo de rota raiz para teste
@app.route('/')
def index():
    return jsonify({"mensagem": "API Barbearia Online"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
