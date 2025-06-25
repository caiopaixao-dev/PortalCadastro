from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import psycopg2
import sqlite3
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta
import bcrypt
import logging
from functools import wraps
import time

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins="*")

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'nimoenergia-secret-2024')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-2024')

def get_db_connection():
    """Obter conexão com banco de dados baseado na configuração"""
    db_type = os.getenv('DATABASE_TYPE', 'sqlite').lower()
    
    try:
        if db_type == 'mysql':
            return mysql.connector.connect(
                host=os.getenv('DATABASE_HOST', 'localhost'),
                user=os.getenv('DATABASE_USER', 'root'),
                password=os.getenv('DATABASE_PASSWORD', ''),
                database=os.getenv('DATABASE_NAME', 'portal_nimoenergia'),
                port=int(os.getenv('DATABASE_PORT', 3306))
            )
        elif db_type == 'postgresql':
            return psycopg2.connect(
                host=os.getenv('DATABASE_HOST', 'localhost'),
                user=os.getenv('DATABASE_USER', 'postgres'),
                password=os.getenv('DATABASE_PASSWORD', ''),
                database=os.getenv('DATABASE_NAME', 'portal_nimoenergia'),
                port=int(os.getenv('DATABASE_PORT', 5432))
            )
        else:  # SQLite
            db_name = os.getenv('DATABASE_NAME', 'portal_nimoenergia.db')
            if db_name == ':memory:':
                return sqlite3.connect(':memory:', check_same_thread=False)
            return sqlite3.connect(db_name, check_same_thread=False)
    except Exception as e:
        logger.error(f"Erro ao conectar com banco de dados: {e}")
        return None

def require_auth(f):
    """Decorator para rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token de acesso requerido'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    """Endpoint principal da API"""
    return jsonify({
        'message': 'Portal NIMOENERGIA Backend API',
        'version': '2.0.0',
        'status': 'online',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/health')
def health_check():
    """Endpoint de health check para monitoramento"""
    try:
        # Testar conexão com banco
        conn = get_db_connection()
        db_status = 'connected' if conn else 'disconnected'
        if conn:
            conn.close()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '2.0.0',
            'database': db_status,
            'environment': os.getenv('FLASK_ENV', 'production'),
            'uptime': time.time()
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Endpoint de autenticação"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados JSON requeridos'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        # Usuários de teste (em produção, consultar banco de dados)
        test_users = {
            'admin@nimoenergia.com.br': {
                'password': 'senha123',
                'nome': 'Admin NIMO',
                'tipo': 'admin'
            },
            'silva@silvatransportes.com.br': {
                'password': 'senha123',
                'nome': 'Silva Transportes',
                'tipo': 'transportadora'
            }
        }
        
        if email in test_users and test_users[email]['password'] == password:
            user_data = test_users[email]
            
            # Gerar token JWT
            token = jwt.encode({
                'email': email,
                'nome': user_data['nome'],
                'tipo': user_data['tipo'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['JWT_SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                'token': token,
                'user': {
                    'email': email,
                    'nome': user_data['nome'],
                    'tipo': user_data['tipo']
                }
            })
        else:
            return jsonify({'error': 'Credenciais inválidas'}), 401
            
    except Exception as e:
        logger.error(f"Erro no login: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """Endpoint de dados do dashboard"""
    try:
        # Em produção, consultar banco de dados real
        dashboard_data = {
            'total_documentos': 156,
            'documentos_pendentes': 12,
            'documentos_aprovados': 128,
            'documentos_rejeitados': 16,
            'transportadoras_ativas': 8,
            'transportadoras_total': 15,
            'ultima_atualizacao': datetime.utcnow().isoformat()
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        logger.error(f"Erro no dashboard: {e}")
        return jsonify({'error': 'Erro ao carregar dados do dashboard'}), 500

@app.route('/api/documentos', methods=['GET'])
def listar_documentos():
    """Endpoint para listar documentos"""
    try:
        # Em produção, consultar banco de dados
        documentos = [
            {
                'id': 1,
                'nome': 'Licença de Operação - Silva Transportes',
                'tipo': 'licenca_operacao',
                'status': 'aprovado',
                'data_upload': '2024-01-15T10:30:00Z',
                'transportadora': 'Silva Transportes'
            },
            {
                'id': 2,
                'nome': 'Seguro Veicular - Frota 001',
                'tipo': 'seguro_veicular',
                'status': 'pendente',
                'data_upload': '2024-01-16T14:20:00Z',
                'transportadora': 'Silva Transportes'
            }
        ]
        
        return jsonify(documentos)
        
    except Exception as e:
        logger.error(f"Erro ao listar documentos: {e}")
        return jsonify({'error': 'Erro ao carregar documentos'}), 500

@app.route('/api/tipos-documentos', methods=['GET'])
def tipos_documentos():
    """Endpoint para listar tipos de documentos aceitos"""
    try:
        tipos = [
            {
                'id': 'licenca_operacao',
                'nome': 'Licença de Operação',
                'descricao': 'Licença para operação de transporte',
                'formatos_aceitos': ['PDF', 'JPG', 'PNG']
            },
            {
                'id': 'seguro_veicular',
                'nome': 'Seguro Veicular',
                'descricao': 'Apólice de seguro dos veículos',
                'formatos_aceitos': ['PDF', 'JPG', 'PNG']
            },
            {
                'id': 'cnh_motorista',
                'nome': 'CNH do Motorista',
                'descricao': 'Carteira Nacional de Habilitação',
                'formatos_aceitos': ['PDF', 'JPG', 'PNG']
            }
        ]
        
        return jsonify(tipos)
        
    except Exception as e:
        logger.error(f"Erro ao listar tipos de documentos: {e}")
        return jsonify({'error': 'Erro ao carregar tipos de documentos'}), 500

@app.route('/api/upload', methods=['POST'])
def upload_documento():
    """Endpoint para upload de documentos"""
    try:
        if 'arquivo' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        arquivo = request.files['arquivo']
        tipo_documento = request.form.get('tipo_documento')
        
        if arquivo.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not tipo_documento:
            return jsonify({'error': 'Tipo de documento é obrigatório'}), 400
        
        # Em produção, salvar arquivo e registrar no banco
        return jsonify({
            'message': 'Documento enviado com sucesso',
            'id': 123,
            'nome_arquivo': arquivo.filename,
            'tipo_documento': tipo_documento,
            'status': 'pendente'
        })
        
    except Exception as e:
        logger.error(f"Erro no upload: {e}")
        return jsonify({'error': 'Erro ao fazer upload do documento'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handler para rotas não encontradas"""
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handler para métodos não permitidos"""
    return jsonify({'error': 'Método não permitido'}), 405

@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos"""
    logger.error(f"Erro interno: {error}")
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Iniciando Portal NIMOENERGIA na porta {port}")
    logger.info(f"Modo debug: {debug}")
    logger.info(f"Banco de dados: {os.getenv('DATABASE_TYPE', 'sqlite')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

