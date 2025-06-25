-- =====================================================
-- PORTAL NIMOENERGIA - ESTRUTURA MYSQL COMPLETA
-- Sistema de Gestão de Documentos para Transportadoras
-- Adaptado para MySQL 8.0+
-- =====================================================

-- Configurações iniciais
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

-- =====================================================
-- TABELA: configuracoes
-- Armazena configurações gerais do sistema
-- =====================================================
CREATE TABLE configuracoes (
    id_configuracao INT AUTO_INCREMENT PRIMARY KEY,
    chave VARCHAR(100) UNIQUE NOT NULL,
    valor TEXT NOT NULL,
    descricao TEXT,
    tipo_valor VARCHAR(20) DEFAULT 'string',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (tipo_valor IN ('string', 'integer', 'boolean', 'json'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: tipos_documento
-- Define os tipos de documentos aceitos no sistema
-- =====================================================
CREATE TABLE tipos_documento (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    nome_tipo VARCHAR(100) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(50) NOT NULL,
    subcategoria VARCHAR(50),
    obrigatorio_vencimento BOOLEAN DEFAULT FALSE,
    obrigatorio_garantia BOOLEAN DEFAULT FALSE,
    formatos_aceitos JSON DEFAULT ('["PDF", "DOCX", "JPG", "PNG"]'),
    tamanho_maximo_mb INT DEFAULT 10,
    aprovacao_automatica BOOLEAN DEFAULT FALSE,
    dias_aviso_vencimento INT DEFAULT 30,
    dias_tolerancia INT DEFAULT 5,
    ativo BOOLEAN DEFAULT TRUE,
    ordem_exibicao INT DEFAULT 0,
    icone VARCHAR(50),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (categoria IN ('EMPRESA', 'SEGUROS', 'AMBIENTAL'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: transportadoras
-- Armazena dados das empresas transportadoras
-- =====================================================
CREATE TABLE transportadoras (
    id_transportadora INT AUTO_INCREMENT PRIMARY KEY,
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
    responsavel_tecnico VARCHAR(100),
    responsavel_financeiro VARCHAR(100),
    banco VARCHAR(100),
    agencia VARCHAR(10),
    conta VARCHAR(20),
    status_ativo BOOLEAN DEFAULT TRUE,
    classificacao_risco VARCHAR(10) DEFAULT 'BAIXO',
    limite_credito DECIMAL(15,2),
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (classificacao_risco IN ('BAIXO', 'MEDIO', 'ALTO'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: usuarios
-- Armazena dados dos usuários do sistema
-- =====================================================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_transportadora INT,
    nome_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(50) NOT NULL,
    telefone VARCHAR(20),
    tipo_usuario VARCHAR(20) NOT NULL,
    status_ativo BOOLEAN DEFAULT TRUE,
    ultimo_acesso TIMESTAMP NULL,
    ip_ultimo_acesso VARCHAR(45),
    tentativas_login INT DEFAULT 0,
    bloqueado_ate TIMESTAMP NULL,
    preferencias_notificacao JSON DEFAULT ('{"email": true, "sms": false, "push": true}'),
    timezone VARCHAR(50) DEFAULT 'America/Sao_Paulo',
    idioma VARCHAR(5) DEFAULT 'pt-BR',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (tipo_usuario IN ('ADMIN', 'ANALISTA', 'TRANSPORTADORA')),
    FOREIGN KEY (id_transportadora) REFERENCES transportadoras(id_transportadora) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: documentos
-- Armazena informações dos documentos enviados
-- =====================================================
CREATE TABLE documentos (
    id_documento INT AUTO_INCREMENT PRIMARY KEY,
    numero_protocolo VARCHAR(20) UNIQUE NOT NULL,
    id_transportadora INT NOT NULL,
    id_tipo_documento INT NOT NULL,
    id_usuario_upload INT NOT NULL,
    nome_arquivo_original VARCHAR(255) NOT NULL,
    nome_arquivo_sistema VARCHAR(255) NOT NULL,
    caminho_arquivo TEXT NOT NULL,
    tamanho_arquivo BIGINT NOT NULL,
    hash_arquivo VARCHAR(64) NOT NULL,
    mime_type VARCHAR(100),
    data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_vencimento DATE,
    valor_garantia DECIMAL(15,2),
    status_documento VARCHAR(20) DEFAULT 'PENDENTE',
    data_aprovacao TIMESTAMP NULL,
    id_usuario_aprovacao INT,
    observacoes_analista TEXT,
    motivo_rejeicao TEXT,
    versao_documento INT DEFAULT 1,
    id_documento_anterior INT,
    ip_upload VARCHAR(45),
    user_agent TEXT,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (status_documento IN ('PENDENTE', 'APROVADO', 'REJEITADO', 'VENCIDO', 'RENOVACAO')),
    FOREIGN KEY (id_transportadora) REFERENCES transportadoras(id_transportadora) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo_documento) REFERENCES tipos_documento(id_tipo) ON DELETE RESTRICT,
    FOREIGN KEY (id_usuario_upload) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    FOREIGN KEY (id_usuario_aprovacao) REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    FOREIGN KEY (id_documento_anterior) REFERENCES documentos(id_documento) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: historico_documentos
-- Registra todas as ações realizadas nos documentos
-- =====================================================
CREATE TABLE historico_documentos (
    id_historico INT AUTO_INCREMENT PRIMARY KEY,
    id_documento INT NOT NULL,
    id_usuario INT NOT NULL,
    acao VARCHAR(50) NOT NULL,
    status_anterior VARCHAR(20),
    status_novo VARCHAR(20),
    observacoes TEXT,
    dados_alteracao JSON,
    ip_origem VARCHAR(45),
    data_acao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_documento) REFERENCES documentos(id_documento) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA: notificacoes
-- Gerencia notificações enviadas aos usuários
-- =====================================================
CREATE TABLE notificacoes (
    id_notificacao INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_documento INT,
    tipo_notificacao VARCHAR(50) NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    mensagem TEXT NOT NULL,
    canal VARCHAR(20) DEFAULT 'EMAIL',
    status_envio VARCHAR(20) DEFAULT 'PENDENTE',
    data_envio TIMESTAMP NULL,
    data_leitura TIMESTAMP NULL,
    tentativas_envio INT DEFAULT 0,
    erro_envio TEXT,
    dados_extras JSON,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (canal IN ('EMAIL', 'SMS', 'PUSH', 'SISTEMA')),
    CHECK (status_envio IN ('PENDENTE', 'ENVIADO', 'ERRO', 'LIDO')),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_documento) REFERENCES documentos(id_documento) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- ÍNDICES PARA PERFORMANCE
-- =====================================================
CREATE INDEX idx_configuracoes_chave ON configuracoes(chave);
CREATE INDEX idx_tipos_documento_categoria ON tipos_documento(categoria);
CREATE INDEX idx_tipos_documento_ativo ON tipos_documento(ativo);
CREATE INDEX idx_transportadoras_cnpj ON transportadoras(cnpj);
CREATE INDEX idx_transportadoras_razao_social ON transportadoras(razao_social);
CREATE INDEX idx_transportadoras_status_ativo ON transportadoras(status_ativo);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_tipo ON usuarios(tipo_usuario);
CREATE INDEX idx_usuarios_transportadora ON usuarios(id_transportadora);
CREATE INDEX idx_documentos_protocolo ON documentos(numero_protocolo);
CREATE INDEX idx_documentos_transportadora ON documentos(id_transportadora);
CREATE INDEX idx_documentos_tipo ON documentos(id_tipo_documento);
CREATE INDEX idx_documentos_status ON documentos(status_documento);
CREATE INDEX idx_documentos_data_upload ON documentos(data_upload);
CREATE INDEX idx_documentos_data_vencimento ON documentos(data_vencimento);
CREATE INDEX idx_historico_documento ON historico_documentos(id_documento);
CREATE INDEX idx_historico_usuario ON historico_documentos(id_usuario);
CREATE INDEX idx_notificacoes_usuario ON notificacoes(id_usuario);
CREATE INDEX idx_notificacoes_status_envio ON notificacoes(status_envio);

-- =====================================================
-- DADOS INICIAIS
-- =====================================================

-- Inserir tipos de documentos padrão
INSERT INTO tipos_documento (nome_tipo, descricao, categoria, obrigatorio_vencimento, ativo) VALUES
('Alvará de Funcionamento', 'Documento que autoriza o funcionamento da empresa', 'EMPRESA', TRUE, TRUE),
('Contrato Social', 'Documento de constituição da empresa', 'EMPRESA', FALSE, TRUE),
('Inscrição Estadual', 'Documento de inscrição no estado', 'EMPRESA', FALSE, TRUE),
('Seguro de Responsabilidade Civil', 'Seguro obrigatório para transportadoras', 'SEGUROS', TRUE, TRUE),
('Seguro de Carga', 'Seguro para proteção da carga transportada', 'SEGUROS', TRUE, TRUE),
('Licença Ambiental', 'Licença para operação com impacto ambiental', 'AMBIENTAL', TRUE, TRUE),
('Certificado ISO', 'Certificação de qualidade ISO', 'EMPRESA', TRUE, TRUE);

-- Inserir configurações padrão
INSERT INTO configuracoes (chave, valor, descricao, tipo_valor) VALUES
('sistema_nome', 'Portal NIMOENERGIA', 'Nome do sistema', 'string'),
('sistema_versao', '1.0.0', 'Versão atual do sistema', 'string'),
('email_notificacoes', 'noreply@nimoenergia.com.br', 'Email para envio de notificações', 'string'),
('dias_aviso_vencimento', '30', 'Dias de antecedência para aviso de vencimento', 'integer'),
('tamanho_maximo_arquivo', '10', 'Tamanho máximo de arquivo em MB', 'integer'),
('backup_automatico', 'true', 'Ativar backup automático', 'boolean');

-- Inserir usuário administrador padrão
INSERT INTO usuarios (nome_completo, email, senha_hash, salt, tipo_usuario, status_ativo) VALUES
('Administrador Sistema', 'admin@nimoenergia.com.br', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PmvlJO', 'salt123', 'ADMIN', TRUE);

-- Finalizar transação
SET FOREIGN_KEY_CHECKS = 1;
COMMIT;

