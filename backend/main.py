from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import jwt
import bcrypt
import logging
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import uuid
import hashlib
from dotenv import load_dotenv
from database_manager import db_manager

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Inicialização da aplicação
app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Configurações de segurança
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'nimoenergia-secret-2024-ultra-secure')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-nimoenergia-2024')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif'}

# Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per hour", "100 per minute"]
)

# Middleware de segurança
@app.before_request
def security_headers():
    """Adiciona headers de segurança"""
    g.request_id = str(uuid.uuid4())
    g.start_time = datetime.utcnow()
    
    # Log da requisição
    logger.info(f"Request {g.request_id}: {request.method} {request.path} from {request.remote_addr}")

@app.after_request
def after_request(response):
    """Adiciona headers de segurança e logs de resposta"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Request-ID'] = g.request_id
    
    # Log da resposta
    duration = (datetime.utcnow() - g.start_time).total_seconds()
    logger.info(f"Response {g.request_id}: {response.status_code} in {duration:.3f}s")
    
    return response

# Utilitários de segurança
class SecurityUtils:
    @staticmethod
    def hash_password(password):
        """Gera hash seguro da senha"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed):
        """Verifica senha contra hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def generate_token(user_data, expires_hours=24):
        """Gera token JWT"""
        payload = {
            'user_id': user_data.get('id'),
            'email': user_data.get('email'),
            'tipo': user_data.get('tipo'),
            'transportadora_id': user_data.get('transportadora_id'),
            'exp': datetime.utcnow() + timedelta(hours=expires_hours),
            'iat': datetime.utcnow(),
            'jti': str(uuid.uuid4())  # JWT ID único
        }
        return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        """Verifica e decodifica token JWT"""
        try:
            payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return {'error': 'Token expirado'}
        except jwt.InvalidTokenError:
            return {'error': 'Token inválido'}

# Decoradores de autenticação e autorização
def token_required(f):
    """Decorator para rotas que requerem autenticação"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token não fornecido'}), 401
        
        try:
            token = auth_header.split(' ')[1]  # Bearer <token>
            payload = SecurityUtils.verify_token(token)
            if 'error' in payload:
                return jsonify(payload), 401
            g.current_user = payload
        except IndexError:
            return jsonify({'error': 'Formato de token inválido'}), 401
        
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator para rotas que requerem privilégios de admin"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.current_user.get('tipo') != 'admin':
            return jsonify({'error': 'Acesso negado - privilégios de administrador necessários'}), 403
        return f(*args, **kwargs)
    return decorated

# Validadores de entrada
class InputValidator:
    @staticmethod
    def validate_email(email):
        """Valida formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_cnpj(cnpj):
        """Valida formato de CNPJ"""
        import re
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        return len(cnpj) == 14
    
    @staticmethod
    def validate_password(password):
        """Valida força da senha"""
        if len(password) < 8:
            return False, "Senha deve ter pelo menos 8 caracteres"
        if not any(c.isupper() for c in password):
            return False, "Senha deve ter pelo menos uma letra maiúscula"
        if not any(c.islower() for c in password):
            return False, "Senha deve ter pelo menos uma letra minúscula"
        if not any(c.isdigit() for c in password):
            return False, "Senha deve ter pelo menos um número"
        return True, "Senha válida"

# Serviços de negócio
class UserService:
    @staticmethod
    def create_user(data):
        """Cria novo usuário"""
        try:
            # Validações
            if not InputValidator.validate_email(data.get('email')):
                return {'error': 'Email inválido'}, 400
            
            password_valid, password_msg = InputValidator.validate_password(data.get('password', ''))
            if not password_valid:
                return {'error': password_msg}, 400
            
            # Verificar se email já existe
            existing_user = db_manager.execute_query(
                "SELECT id FROM usuarios WHERE email = %s" if db_manager.db_type != 'sqlite' 
                else "SELECT id FROM usuarios WHERE email = ?",
                (data['email'],),
                fetch=True
            )
            
            if existing_user:
                return {'error': 'Email já cadastrado'}, 400
            
            # Hash da senha
            hashed_password = SecurityUtils.hash_password(data['password'])
            
            # Inserir usuário
            user_id = db_manager.execute_query(
                """INSERT INTO usuarios (transportadora_id, nome, email, senha, tipo, ativo) 
                   VALUES (%s, %s, %s, %s, %s, %s)""" if db_manager.db_type != 'sqlite'
                else """INSERT INTO usuarios (transportadora_id, nome, email, senha, tipo, ativo) 
                        VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    data.get('transportadora_id'),
                    data['nome'],
                    data['email'],
                    hashed_password,
                    data.get('tipo', 'transportadora'),
                    True
                )
            )
            
            logger.info(f"Usuário criado: {data['email']} (ID: {user_id})")
            return {'message': 'Usuário criado com sucesso', 'user_id': user_id}, 201
            
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            return {'error': 'Erro interno do servidor'}, 500
    
    @staticmethod
    def authenticate_user(email, password):
        """Autentica usuário"""
        try:
            # Buscar usuário
            user = db_manager.execute_query(
                """SELECT u.*, t.nome as transportadora_nome 
                   FROM usuarios u 
                   LEFT JOIN transportadoras t ON u.transportadora_id = t.id 
                   WHERE u.email = %s AND u.ativo = %s""" if db_manager.db_type != 'sqlite'
                else """SELECT u.*, t.nome as transportadora_nome 
                        FROM usuarios u 
                        LEFT JOIN transportadoras t ON u.transportadora_id = t.id 
                        WHERE u.email = ? AND u.ativo = ?""",
                (email, True),
                fetch=True
            )
            
            if not user:
                return {'error': 'Credenciais inválidas'}, 401
            
            user = user[0]
            
            # Verificar senha
            if not SecurityUtils.verify_password(password, user['senha']):
                return {'error': 'Credenciais inválidas'}, 401
            
            # Atualizar último acesso
            db_manager.execute_query(
                "UPDATE usuarios SET ultimo_acesso = %s WHERE id = %s" if db_manager.db_type != 'sqlite'
                else "UPDATE usuarios SET ultimo_acesso = ? WHERE id = ?",
                (datetime.utcnow(), user['id'])
            )
            
            # Gerar token
            token = SecurityUtils.generate_token(user)
            
            logger.info(f"Login realizado: {email}")
            
            return {
                'token': token,
                'user': {
                    'id': user['id'],
                    'nome': user['nome'],
                    'email': user['email'],
                    'tipo': user['tipo'],
                    'transportadora_id': user.get('transportadora_id'),
                    'transportadora_nome': user.get('transportadora_nome')
                }
            }, 200
            
        except Exception as e:
            logger.error(f"Erro na autenticação: {str(e)}")
            return {'error': 'Erro interno do servidor'}, 500

class TransportadoraService:
    @staticmethod
    def create_transportadora(data):
        """Cria nova transportadora"""
        try:
            # Validações
            if not InputValidator.validate_cnpj(data.get('cnpj')):
                return {'error': 'CNPJ inválido'}, 400
            
            # Verificar se CNPJ já existe
            existing = db_manager.execute_query(
                "SELECT id FROM transportadoras WHERE cnpj = %s" if db_manager.db_type != 'sqlite'
                else "SELECT id FROM transportadoras WHERE cnpj = ?",
                (data['cnpj'],),
                fetch=True
            )
            
            if existing:
                return {'error': 'CNPJ já cadastrado'}, 400
            
            # Inserir transportadora
            transportadora_id = db_manager.execute_query(
                """INSERT INTO transportadoras (cnpj, nome, email, telefone, endereco, ativo) 
                   VALUES (%s, %s, %s, %s, %s, %s)""" if db_manager.db_type != 'sqlite'
                else """INSERT INTO transportadoras (cnpj, nome, email, telefone, endereco, ativo) 
                        VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    data['cnpj'],
                    data['nome'],
                    data.get('email'),
                    data.get('telefone'),
                    data.get('endereco'),
                    True
                )
            )
            
            logger.info(f"Transportadora criada: {data['nome']} (ID: {transportadora_id})")
            return {'message': 'Transportadora cadastrada com sucesso', 'transportadora_id': transportadora_id}, 201
            
        except Exception as e:
            logger.error(f"Erro ao criar transportadora: {str(e)}")
            return {'error': 'Erro interno do servidor'}, 500

# Rotas da API
@app.route('/')
def home():
    """Endpoint de status da API"""
    return jsonify({
        'message': 'Portal NIMOENERGIA Backend API',
        'version': '2.0.0',
        'status': 'online',
        'database': db_manager.db_type,
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            'auth': '/api/auth/login',
            'users': '/api/users',
            'transportadoras': '/api/transportadoras',
            'documentos': '/api/documentos',
            'dashboard': '/api/dashboard',
            'health': '/api/health'
        }
    })

@app.route('/api/health')
def health_check():
    """Endpoint de health check"""
    try:
        # Testar conexão com banco
        db_manager.execute_query("SELECT 1" if db_manager.db_type != 'sqlite' else "SELECT 1", fetch=True)
        db_status = 'healthy'
    except:
        db_status = 'unhealthy'
    
    return jsonify({
        'status': 'healthy' if db_status == 'healthy' else 'degraded',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat(),
        'uptime': 'N/A'  # Implementar contador de uptime se necessário
    })

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Endpoint de autenticação"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        result, status_code = UserService.authenticate_user(data['email'], data['password'])
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Erro no login: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/users', methods=['POST'])
@limiter.limit("5 per minute")
def create_user():
    """Endpoint para criar usuário"""
    try:
        data = request.get_json()
        
        required_fields = ['nome', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        result, status_code = UserService.create_user(data)
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/transportadoras', methods=['POST'])
@token_required
def create_transportadora():
    """Endpoint para criar transportadora"""
    try:
        data = request.get_json()
        
        required_fields = ['cnpj', 'nome']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        result, status_code = TransportadoraService.create_transportadora(data)
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Erro ao criar transportadora: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/transportadoras', methods=['GET'])
@token_required
@admin_required
def list_transportadoras():
    """Lista todas as transportadoras (apenas admin)"""
    try:
        transportadoras = db_manager.execute_query(
            "SELECT * FROM transportadoras WHERE ativo = %s ORDER BY nome" if db_manager.db_type != 'sqlite'
            else "SELECT * FROM transportadoras WHERE ativo = ? ORDER BY nome",
            (True,),
            fetch=True
        )
        
        return jsonify(transportadoras or [])
        
    except Exception as e:
        logger.error(f"Erro ao listar transportadoras: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/dashboard', methods=['GET'])
@token_required
def dashboard():
    """Endpoint do dashboard"""
    try:
        user_tipo = g.current_user.get('tipo')
        transportadora_id = g.current_user.get('transportadora_id')
        
        if user_tipo == 'admin':
            # Dashboard administrativo
            stats = db_manager.execute_query(
                """SELECT 
                    (SELECT COUNT(*) FROM transportadoras WHERE ativo = %s) as total_transportadoras,
                    (SELECT COUNT(*) FROM usuarios WHERE ativo = %s) as total_usuarios,
                    (SELECT COUNT(*) FROM documentos) as total_documentos,
                    (SELECT COUNT(*) FROM documentos WHERE status = %s) as documentos_pendentes
                """ if db_manager.db_type != 'sqlite' else
                """SELECT 
                    (SELECT COUNT(*) FROM transportadoras WHERE ativo = ?) as total_transportadoras,
                    (SELECT COUNT(*) FROM usuarios WHERE ativo = ?) as total_usuarios,
                    (SELECT COUNT(*) FROM documentos) as total_documentos,
                    (SELECT COUNT(*) FROM documentos WHERE status = ?) as documentos_pendentes
                """,
                (True, True, 'pendente'),
                fetch=True
            )
        else:
            # Dashboard da transportadora
            stats = db_manager.execute_query(
                """SELECT 
                    (SELECT COUNT(*) FROM documentos WHERE transportadora_id = %s) as meus_documentos,
                    (SELECT COUNT(*) FROM documentos WHERE transportadora_id = %s AND status = %s) as documentos_pendentes,
                    (SELECT COUNT(*) FROM documentos WHERE transportadora_id = %s AND status = %s) as documentos_aprovados
                """ if db_manager.db_type != 'sqlite' else
                """SELECT 
                    (SELECT COUNT(*) FROM documentos WHERE transportadora_id = ?) as meus_documentos,
                    (SELECT COUNT(*) FROM documentos WHERE transportadora_id = ? AND status = ?) as documentos_pendentes,
                    (SELECT COUNT(*) FROM documentos WHERE transportadora_id = ? AND status = ?) as documentos_aprovados
                """,
                (transportadora_id, transportadora_id, 'pendente', transportadora_id, 'aprovado'),
                fetch=True
            )
        
        return jsonify(stats[0] if stats else {})
        
    except Exception as e:
        logger.error(f"Erro no dashboard: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/tipos-documentos', methods=['GET'])
def tipos_documentos():
    """Lista tipos de documentos"""
    try:
        tipos = db_manager.execute_query(
            "SELECT * FROM tipos_documento WHERE ativo = %s ORDER BY nome" if db_manager.db_type != 'sqlite'
            else "SELECT * FROM tipos_documento WHERE ativo = ? ORDER BY nome",
            (True,),
            fetch=True
        )
        
        return jsonify(tipos or [])
        
    except Exception as e:
        logger.error(f"Erro ao listar tipos de documentos: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Tratamento de erros
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Método não permitido'}), 405

@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def too_large(error):
    return jsonify({'error': 'Arquivo muito grande'}), 413

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Muitas requisições. Tente novamente mais tarde.'}), 429

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erro interno: {str(error)}")
    return jsonify({'error': 'Erro interno do servidor'}), 500

# Inicialização
def initialize_app():
    """Inicializa a aplicação"""
    try:
        # Criar tabelas se não existirem
        db_manager.create_tables()
        
        # Inserir dados iniciais
        db_manager.insert_sample_data()
        
        # Criar pasta de uploads
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        logger.info("Aplicação inicializada com sucesso")
        
    except Exception as e:
        logger.error(f"Erro na inicialização: {str(e)}")
        raise

if __name__ == '__main__':
    initialize_app()
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Iniciando servidor na porta {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)

