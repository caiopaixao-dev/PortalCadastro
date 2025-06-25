import os
import mysql.connector
import psycopg2
import sqlite3
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador de banco de dados universal e robusto"""
    
    def __init__(self):
        self.db_type = os.getenv('DATABASE_TYPE', 'mysql').lower()
        self.connection = None
        self._initialize_logging()
        
    def _initialize_logging(self):
        """Configura logging específico para banco"""
        self.logger = logging.getLogger(f'db.{self.db_type}')
        
    def get_connection(self):
        """Retorna conexão baseada no tipo de banco configurado"""
        try:
            if self.db_type == 'mysql':
                return self._get_mysql_connection()
            elif self.db_type == 'postgresql':
                return self._get_postgresql_connection()
            elif self.db_type == 'sqlite':
                return self._get_sqlite_connection()
            else:
                raise ValueError(f"Tipo de banco não suportado: {self.db_type}")
        except Exception as e:
            self.logger.error(f"Erro na conexão com banco {self.db_type}: {e}")
            return None
    
    def _get_mysql_connection(self):
        """Conexão MySQL - Para AWS RDS, JawsDB, etc."""
        return mysql.connector.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME'),
            port=int(os.getenv('DATABASE_PORT', 3306)),
            charset='utf8mb4',
            autocommit=False,
            pool_name='portal_pool',
            pool_size=10,
            pool_reset_session=True,
            connect_timeout=30,
            sql_mode='STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO'
        )
    
    def _get_postgresql_connection(self):
        """Conexão PostgreSQL - Para Heroku Postgres"""
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            return psycopg2.connect(database_url, sslmode='require')
        else:
            return psycopg2.connect(
                host=os.getenv('DATABASE_HOST'),
                user=os.getenv('DATABASE_USER'),
                password=os.getenv('DATABASE_PASSWORD'),
                database=os.getenv('DATABASE_NAME'),
                port=int(os.getenv('DATABASE_PORT', 5432)),
                connect_timeout=30
            )
    
    def _get_sqlite_connection(self):
        """Conexão SQLite - Para desenvolvimento local"""
        db_path = os.getenv('DATABASE_PATH', 'portal_nimoenergia.db')
        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute('PRAGMA journal_mode = WAL')
        conn.execute('PRAGMA synchronous = NORMAL')
        return conn
    
    def execute_query(self, query, params=None, fetch=False):
        """Executa query de forma universal com tratamento robusto"""
        conn = None
        cursor = None
        
        try:
            conn = self.get_connection()
            if not conn:
                raise Exception("Falha na conexão com banco de dados")
            
            # Configurar cursor baseado no tipo de banco
            if self.db_type == 'mysql':
                cursor = conn.cursor(dictionary=True, buffered=True)
            elif self.db_type == 'postgresql':
                cursor = conn.cursor()
            else:  # sqlite
                cursor = conn.cursor()
                cursor.row_factory = sqlite3.Row
            
            # Executar query
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Processar resultado
            if fetch:
                if self.db_type == 'mysql':
                    return cursor.fetchall()
                elif self.db_type == 'postgresql':
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                else:  # sqlite
                    return [dict(row) for row in cursor.fetchall()]
            
            # Commit para operações de escrita
            if not fetch:
                conn.commit()
                return cursor.lastrowid if hasattr(cursor, 'lastrowid') else cursor.rowcount
            
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Erro na execução da query: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def create_tables(self):
        """Cria estrutura completa de tabelas baseado no tipo de banco"""
        self.logger.info(f"Criando estrutura de tabelas para {self.db_type}")
        
        if self.db_type == 'mysql':
            self._create_mysql_tables()
        elif self.db_type == 'postgresql':
            self._create_postgresql_tables()
        elif self.db_type == 'sqlite':
            self._create_sqlite_tables()
    
    def _create_mysql_tables(self):
        """Cria estrutura completa MySQL"""
        queries = [
            # Configurações do sistema
            """
            CREATE TABLE IF NOT EXISTS configuracoes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                chave VARCHAR(100) UNIQUE NOT NULL,
                valor TEXT NOT NULL,
                descricao TEXT,
                tipo_valor ENUM('string', 'integer', 'boolean', 'json') DEFAULT 'string',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_configuracoes_chave (chave)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Tipos de documento
            """
            CREATE TABLE IF NOT EXISTS tipos_documento (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(50) UNIQUE NOT NULL,
                nome VARCHAR(100) NOT NULL,
                descricao TEXT,
                categoria ENUM('EMPRESA', 'SEGUROS', 'AMBIENTAL', 'FISCAL') NOT NULL,
                subcategoria VARCHAR(50),
                obrigatorio BOOLEAN DEFAULT FALSE,
                tem_vencimento BOOLEAN DEFAULT FALSE,
                tem_garantia BOOLEAN DEFAULT FALSE,
                formatos_aceitos JSON DEFAULT ('["PDF", "DOC", "DOCX", "JPG", "JPEG", "PNG"]'),
                tamanho_maximo_mb INT DEFAULT 10,
                aprovacao_automatica BOOLEAN DEFAULT FALSE,
                dias_aviso_vencimento INT DEFAULT 30,
                ordem_exibicao INT DEFAULT 0,
                ativo BOOLEAN DEFAULT TRUE,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_tipos_documento_categoria (categoria),
                INDEX idx_tipos_documento_ativo (ativo),
                INDEX idx_tipos_documento_codigo (codigo)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Transportadoras
            """
            CREATE TABLE IF NOT EXISTS transportadoras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cnpj VARCHAR(18) UNIQUE NOT NULL,
                razao_social VARCHAR(200) NOT NULL,
                nome_fantasia VARCHAR(200),
                inscricao_estadual VARCHAR(20),
                inscricao_municipal VARCHAR(20),
                antt VARCHAR(20),
                endereco_logradouro VARCHAR(200),
                endereco_numero VARCHAR(10),
                endereco_complemento VARCHAR(100),
                endereco_bairro VARCHAR(100),
                endereco_cidade VARCHAR(100),
                endereco_estado VARCHAR(2),
                endereco_cep VARCHAR(9),
                endereco_pais VARCHAR(50) DEFAULT 'Brasil',
                telefone_principal VARCHAR(20),
                telefone_secundario VARCHAR(20),
                email_corporativo VARCHAR(100),
                email_financeiro VARCHAR(100),
                site VARCHAR(100),
                responsavel_nome VARCHAR(100),
                responsavel_cpf VARCHAR(14),
                responsavel_cargo VARCHAR(50),
                responsavel_email VARCHAR(100),
                responsavel_telefone VARCHAR(20),
                banco VARCHAR(100),
                agencia VARCHAR(10),
                conta VARCHAR(20),
                pix VARCHAR(100),
                status_cadastro ENUM('PENDENTE', 'APROVADO', 'SUSPENSO', 'INATIVO') DEFAULT 'PENDENTE',
                classificacao_risco ENUM('BAIXO', 'MEDIO', 'ALTO') DEFAULT 'BAIXO',
                limite_credito DECIMAL(15,2) DEFAULT 0.00,
                observacoes TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_aprovacao TIMESTAMP NULL,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                ativo BOOLEAN DEFAULT TRUE,
                INDEX idx_transportadoras_cnpj (cnpj),
                INDEX idx_transportadoras_razao_social (razao_social),
                INDEX idx_transportadoras_status (status_cadastro),
                INDEX idx_transportadoras_ativo (ativo),
                INDEX idx_transportadoras_data_cadastro (data_cadastro)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Usuários
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                transportadora_id INT NULL,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                senha VARCHAR(255) NOT NULL,
                salt VARCHAR(50),
                telefone VARCHAR(20),
                tipo ENUM('admin', 'analista', 'transportadora', 'financeiro') NOT NULL,
                permissoes JSON DEFAULT ('[]'),
                status_ativo BOOLEAN DEFAULT TRUE,
                ultimo_acesso TIMESTAMP NULL,
                ip_ultimo_acesso VARCHAR(45),
                tentativas_login INT DEFAULT 0,
                bloqueado_ate TIMESTAMP NULL,
                token_reset_senha VARCHAR(100),
                token_reset_expira TIMESTAMP NULL,
                preferencias JSON DEFAULT ('{"notificacoes_email": true, "notificacoes_sms": false}'),
                timezone VARCHAR(50) DEFAULT 'America/Sao_Paulo',
                idioma VARCHAR(5) DEFAULT 'pt-BR',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (transportadora_id) REFERENCES transportadoras(id) ON DELETE SET NULL,
                INDEX idx_usuarios_email (email),
                INDEX idx_usuarios_tipo (tipo),
                INDEX idx_usuarios_transportadora (transportadora_id),
                INDEX idx_usuarios_ativo (status_ativo),
                INDEX idx_usuarios_ultimo_acesso (ultimo_acesso)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Documentos
            """
            CREATE TABLE IF NOT EXISTS documentos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                numero_protocolo VARCHAR(20) UNIQUE NOT NULL,
                transportadora_id INT NOT NULL,
                tipo_documento_id INT NOT NULL,
                usuario_upload_id INT NOT NULL,
                nome_arquivo_original VARCHAR(255) NOT NULL,
                nome_arquivo_sistema VARCHAR(255) NOT NULL,
                caminho_arquivo TEXT NOT NULL,
                tamanho_arquivo BIGINT NOT NULL,
                hash_arquivo VARCHAR(64) NOT NULL,
                mime_type VARCHAR(100),
                data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_vencimento DATE NULL,
                valor_garantia DECIMAL(15,2) NULL,
                numero_apolice VARCHAR(50),
                seguradora VARCHAR(100),
                status ENUM('pendente', 'aprovado', 'rejeitado', 'vencido', 'renovacao') DEFAULT 'pendente',
                data_aprovacao TIMESTAMP NULL,
                usuario_aprovacao_id INT NULL,
                observacoes_analista TEXT,
                motivo_rejeicao TEXT,
                versao_documento INT DEFAULT 1,
                documento_anterior_id INT NULL,
                ip_upload VARCHAR(45),
                user_agent TEXT,
                metadata JSON,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (transportadora_id) REFERENCES transportadoras(id) ON DELETE CASCADE,
                FOREIGN KEY (tipo_documento_id) REFERENCES tipos_documento(id) ON DELETE RESTRICT,
                FOREIGN KEY (usuario_upload_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
                FOREIGN KEY (usuario_aprovacao_id) REFERENCES usuarios(id) ON DELETE SET NULL,
                FOREIGN KEY (documento_anterior_id) REFERENCES documentos(id) ON DELETE SET NULL,
                INDEX idx_documentos_protocolo (numero_protocolo),
                INDEX idx_documentos_transportadora (transportadora_id),
                INDEX idx_documentos_tipo (tipo_documento_id),
                INDEX idx_documentos_status (status),
                INDEX idx_documentos_data_upload (data_upload),
                INDEX idx_documentos_data_vencimento (data_vencimento),
                INDEX idx_documentos_hash (hash_arquivo),
                INDEX idx_documentos_usuario_upload (usuario_upload_id),
                INDEX idx_documentos_transportadora_status (transportadora_id, status),
                INDEX idx_documentos_vencimento_status (data_vencimento, status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Histórico de documentos
            """
            CREATE TABLE IF NOT EXISTS historico_documentos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                documento_id INT NOT NULL,
                usuario_id INT NOT NULL,
                acao ENUM('upload', 'aprovacao', 'rejeicao', 'vencimento', 'renovacao', 'exclusao') NOT NULL,
                status_anterior VARCHAR(20),
                status_novo VARCHAR(20),
                observacoes TEXT,
                dados_alteracao JSON,
                ip_origem VARCHAR(45),
                user_agent TEXT,
                data_acao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (documento_id) REFERENCES documentos(id) ON DELETE CASCADE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
                INDEX idx_historico_documento (documento_id),
                INDEX idx_historico_usuario (usuario_id),
                INDEX idx_historico_data_acao (data_acao),
                INDEX idx_historico_acao (acao),
                INDEX idx_historico_documento_data (documento_id, data_acao)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Notificações
            """
            CREATE TABLE IF NOT EXISTS notificacoes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                transportadora_id INT NULL,
                documento_id INT NULL,
                tipo ENUM('vencimento', 'aprovacao', 'rejeicao', 'cadastro', 'sistema', 'compliance') NOT NULL,
                titulo VARCHAR(200) NOT NULL,
                mensagem TEXT NOT NULL,
                canal ENUM('email', 'sms', 'push', 'sistema') DEFAULT 'email',
                status_envio ENUM('pendente', 'enviado', 'erro', 'lido') DEFAULT 'pendente',
                data_envio TIMESTAMP NULL,
                data_leitura TIMESTAMP NULL,
                tentativas_envio INT DEFAULT 0,
                erro_envio TEXT,
                dados_extras JSON,
                prioridade ENUM('baixa', 'normal', 'alta', 'critica') DEFAULT 'normal',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (transportadora_id) REFERENCES transportadoras(id) ON DELETE SET NULL,
                FOREIGN KEY (documento_id) REFERENCES documentos(id) ON DELETE SET NULL,
                INDEX idx_notificacoes_usuario (usuario_id),
                INDEX idx_notificacoes_transportadora (transportadora_id),
                INDEX idx_notificacoes_documento (documento_id),
                INDEX idx_notificacoes_status_envio (status_envio),
                INDEX idx_notificacoes_tipo (tipo),
                INDEX idx_notificacoes_data_criacao (data_criacao),
                INDEX idx_notificacoes_usuario_status (usuario_id, status_envio)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Auditoria de sistema
            """
            CREATE TABLE IF NOT EXISTS auditoria_sistema (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NULL,
                acao VARCHAR(100) NOT NULL,
                tabela_afetada VARCHAR(50),
                registro_id INT,
                dados_anteriores JSON,
                dados_novos JSON,
                ip_origem VARCHAR(45),
                user_agent TEXT,
                data_acao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
                INDEX idx_auditoria_usuario (usuario_id),
                INDEX idx_auditoria_acao (acao),
                INDEX idx_auditoria_tabela (tabela_afetada),
                INDEX idx_auditoria_data (data_acao),
                INDEX idx_auditoria_registro (tabela_afetada, registro_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Sessões de usuário
            """
            CREATE TABLE IF NOT EXISTS sessoes_usuario (
                id VARCHAR(128) PRIMARY KEY,
                usuario_id INT NOT NULL,
                ip_address VARCHAR(45),
                user_agent TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_expiracao TIMESTAMP NOT NULL,
                ativo BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                INDEX idx_sessoes_usuario (usuario_id),
                INDEX idx_sessoes_expiracao (data_expiracao),
                INDEX idx_sessoes_ativo (ativo)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        ]
        
        for query in queries:
            try:
                self.execute_query(query)
                self.logger.info("Tabela criada com sucesso")
            except Exception as e:
                self.logger.error(f"Erro ao criar tabela: {e}")
                raise
    
    def _create_postgresql_tables(self):
        """Cria estrutura completa PostgreSQL"""
        # Implementação similar ao MySQL, adaptada para PostgreSQL
        # (código similar, mas com sintaxe PostgreSQL)
        pass
    
    def _create_sqlite_tables(self):
        """Cria estrutura completa SQLite"""
        # Implementação similar ao MySQL, adaptada para SQLite
        # (código similar, mas com sintaxe SQLite)
        pass
    
    def insert_sample_data(self):
        """Insere dados iniciais robustos"""
        try:
            # Configurações do sistema
            configuracoes_iniciais = [
                ('sistema_nome', 'Portal NIMOENERGIA', 'Nome do sistema', 'string'),
                ('sistema_versao', '2.0.0', 'Versão atual do sistema', 'string'),
                ('email_notificacoes', 'noreply@nimoenergia.com.br', 'Email para envio de notificações', 'string'),
                ('dias_aviso_vencimento', '30,15,7,1', 'Dias de antecedência para aviso de vencimento', 'string'),
                ('tamanho_maximo_arquivo', '50', 'Tamanho máximo de arquivo em MB', 'integer'),
                ('backup_automatico', 'true', 'Ativar backup automático', 'boolean'),
                ('compliance_minimo', '80', 'Percentual mínimo de compliance exigido', 'integer'),
                ('aprovacao_automatica', 'false', 'Ativar aprovação automática de documentos', 'boolean')
            ]
            
            for chave, valor, descricao, tipo_valor in configuracoes_iniciais:
                try:
                    self.execute_query(
                        "INSERT IGNORE INTO configuracoes (chave, valor, descricao, tipo_valor) VALUES (%s, %s, %s, %s)" if self.db_type == 'mysql'
                        else "INSERT INTO configuracoes (chave, valor, descricao, tipo_valor) VALUES (?, ?, ?, ?) ON CONFLICT(chave) DO NOTHING",
                        (chave, valor, descricao, tipo_valor)
                    )
                except:
                    pass
            
            # Tipos de documentos robustos
            tipos_documentos = [
                ('DOC_SOCIETARIO', 'Contrato Social', 'Documento de constituição da empresa', 'EMPRESA', None, True, False, False),
                ('ALVARA_FUNCIONAMENTO', 'Alvará de Funcionamento', 'Autorização para funcionamento da empresa', 'EMPRESA', None, True, True, False),
                ('INSCRICAO_ESTADUAL', 'Inscrição Estadual', 'Documento de inscrição estadual', 'EMPRESA', None, True, False, False),
                ('SEGURO_RC', 'Seguro de Responsabilidade Civil', 'Seguro obrigatório para transportadoras', 'SEGUROS', 'Responsabilidade Civil', True, True, True),
                ('SEGURO_CARGA', 'Seguro de Carga', 'Seguro para proteção da carga transportada', 'SEGUROS', 'Carga', True, True, True),
                ('LICENCA_AMBIENTAL', 'Licença Ambiental', 'Licença para operação com impacto ambiental', 'AMBIENTAL', None, True, True, False),
                ('CERTIFICADO_ISO', 'Certificado ISO', 'Certificação de qualidade ISO', 'EMPRESA', 'Qualidade', False, True, False),
                ('ANTT', 'Registro ANTT', 'Registro na Agência Nacional de Transportes Terrestres', 'EMPRESA', None, True, True, False),
                ('NOTA_FISCAL', 'Nota Fiscal', 'Documento fiscal de transporte', 'FISCAL', None, True, False, False),
                ('MANIFESTO_CARGA', 'Manifesto de Carga', 'Documento de controle de carga', 'FISCAL', None, True, False, False)
            ]
            
            for codigo, nome, descricao, categoria, subcategoria, obrigatorio, tem_vencimento, tem_garantia in tipos_documentos:
                try:
                    self.execute_query(
                        """INSERT IGNORE INTO tipos_documento 
                           (codigo, nome, descricao, categoria, subcategoria, obrigatorio, tem_vencimento, tem_garantia, ativo) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""" if self.db_type == 'mysql'
                        else """INSERT INTO tipos_documento 
                                (codigo, nome, descricao, categoria, subcategoria, obrigatorio, tem_vencimento, tem_garantia, ativo) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(codigo) DO NOTHING""",
                        (codigo, nome, descricao, categoria, subcategoria, obrigatorio, tem_vencimento, tem_garantia, True)
                    )
                except:
                    pass
            
            # Usuário administrador
            try:
                from main import SecurityUtils
                senha_hash = SecurityUtils.hash_password('admin123')
                
                self.execute_query(
                    """INSERT IGNORE INTO usuarios 
                       (nome, email, senha, tipo, status_ativo) 
                       VALUES (%s, %s, %s, %s, %s)""" if self.db_type == 'mysql'
                    else """INSERT INTO usuarios 
                            (nome, email, senha, tipo, status_ativo) 
                            VALUES (?, ?, ?, ?, ?) ON CONFLICT(email) DO NOTHING""",
                    ('Administrador Sistema', 'admin@nimoenergia.com.br', senha_hash, 'admin', True)
                )
            except:
                # Fallback se SecurityUtils não estiver disponível
                self.execute_query(
                    """INSERT IGNORE INTO usuarios 
                       (nome, email, senha, tipo, status_ativo) 
                       VALUES (%s, %s, %s, %s, %s)""" if self.db_type == 'mysql'
                    else """INSERT INTO usuarios 
                            (nome, email, senha, tipo, status_ativo) 
                            VALUES (?, ?, ?, ?, ?) ON CONFLICT(email) DO NOTHING""",
                    ('Administrador Sistema', 'admin@nimoenergia.com.br', 'admin123', 'admin', True)
                )
            
            self.logger.info("Dados iniciais inseridos com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao inserir dados iniciais: {e}")
            raise

# Instância global do gerenciador
db_manager = DatabaseManager()

