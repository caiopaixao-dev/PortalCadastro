# MER Visual - Portal NIMOENERGIA
## Modelo de Entidade-Relacionamento Completo e Detalhado

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           PORTAL NIMOENERGIA - MER VISUAL                      │
│                          Sistema de Gestão de Documentos                       │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┐         ┌─────────────────────────┐
│      CONFIGURACOES      │         │     TIPOS_DOCUMENTO     │
├─────────────────────────┤         ├─────────────────────────┤
│ id (PK)                 │         │ id (PK)                 │
│ chave (UNIQUE)          │         │ codigo (UNIQUE)         │
│ valor                   │         │ nome                    │
│ descricao               │         │ descricao               │
│ tipo_valor              │         │ categoria               │
│ data_criacao            │         │ subcategoria            │
│ data_atualizacao        │         │ obrigatorio             │
└─────────────────────────┘         │ tem_vencimento          │
                                    │ tem_garantia            │
                                    │ formatos_aceitos (JSON) │
                                    │ tamanho_maximo_mb       │
                                    │ aprovacao_automatica    │
                                    │ dias_aviso_vencimento   │
                                    │ ordem_exibicao          │
                                    │ ativo                   │
                                    │ data_criacao            │
                                    └─────────────────────────┘
                                                │
                                                │ 1:N
                                                ▼
┌─────────────────────────┐         ┌─────────────────────────┐
│     TRANSPORTADORAS     │         │       DOCUMENTOS        │
├─────────────────────────┤         ├─────────────────────────┤
│ id (PK)                 │◄────────┤ id (PK)                 │
│ cnpj (UNIQUE)           │ 1:N     │ numero_protocolo (UNIQUE)│
│ razao_social            │         │ transportadora_id (FK)  │
│ nome_fantasia           │         │ tipo_documento_id (FK)  │
│ inscricao_estadual      │         │ usuario_upload_id (FK)  │
│ inscricao_municipal     │         │ nome_arquivo_original   │
│ antt                    │         │ nome_arquivo_sistema    │
│ endereco_logradouro     │         │ caminho_arquivo         │
│ endereco_numero         │         │ tamanho_arquivo         │
│ endereco_complemento    │         │ hash_arquivo            │
│ endereco_bairro         │         │ mime_type               │
│ endereco_cidade         │         │ data_upload             │
│ endereco_estado         │         │ data_vencimento         │
│ endereco_cep            │         │ valor_garantia          │
│ endereco_pais           │         │ numero_apolice          │
│ telefone_principal      │         │ seguradora              │
│ telefone_secundario     │         │ status                  │
│ email_corporativo       │         │ data_aprovacao          │
│ email_financeiro        │         │ usuario_aprovacao_id(FK)│
│ site                    │         │ observacoes_analista    │
│ responsavel_nome        │         │ motivo_rejeicao         │
│ responsavel_cpf         │         │ versao_documento        │
│ responsavel_cargo       │         │ documento_anterior_id(FK)│
│ responsavel_email       │         │ ip_upload               │
│ responsavel_telefone    │         │ user_agent              │
│ banco                   │         │ metadata (JSON)         │
│ agencia                 │         │ data_atualizacao        │
│ conta                   │         └─────────────────────────┘
│ pix                     │                     │
│ status_cadastro         │                     │ 1:N
│ classificacao_risco     │                     ▼
│ limite_credito          │         ┌─────────────────────────┐
│ observacoes             │         │   HISTORICO_DOCUMENTOS  │
│ data_cadastro           │         ├─────────────────────────┤
│ data_aprovacao          │         │ id (PK)                 │
│ data_atualizacao        │         │ documento_id (FK)       │
│ ativo                   │         │ usuario_id (FK)         │
└─────────────────────────┘         │ acao                    │
            │                       │ status_anterior         │
            │ 1:N                   │ status_novo             │
            ▼                       │ observacoes             │
┌─────────────────────────┐         │ dados_alteracao (JSON)  │
│        USUARIOS         │         │ ip_origem               │
├─────────────────────────┤         │ user_agent              │
│ id (PK)                 │─────────┤ data_acao               │
│ transportadora_id (FK)  │ 1:N     └─────────────────────────┘
│ nome                    │
│ email (UNIQUE)          │
│ senha                   │                     ┌─────────────────────────┐
│ salt                    │                     │      NOTIFICACOES       │
│ telefone                │                     ├─────────────────────────┤
│ tipo                    │                     │ id (PK)                 │
│ permissoes (JSON)       │                     │ usuario_id (FK)         │
│ status_ativo            │                     │ transportadora_id (FK)  │
│ ultimo_acesso           │                     │ documento_id (FK)       │
│ ip_ultimo_acesso        │                     │ tipo                    │
│ tentativas_login        │                     │ titulo                  │
│ bloqueado_ate           │                     │ mensagem                │
│ token_reset_senha       │                     │ canal                   │
│ token_reset_expira      │                     │ status_envio            │
│ preferencias (JSON)     │                     │ data_envio              │
│ timezone                │                     │ data_leitura            │
│ idioma                  │                     │ tentativas_envio        │
│ data_criacao            │                     │ erro_envio              │
│ data_atualizacao        │                     │ dados_extras (JSON)    │
└─────────────────────────┘                     │ prioridade              │
            │                                   │ data_criacao            │
            │ 1:N                               └─────────────────────────┘
            ▼                                               ▲
┌─────────────────────────┐                                 │ 1:N
│    AUDITORIA_SISTEMA    │                                 │
├─────────────────────────┤                                 │
│ id (PK)                 │                                 │
│ usuario_id (FK)         │─────────────────────────────────┘
│ acao                    │
│ tabela_afetada          │
│ registro_id             │
│ dados_anteriores (JSON) │
│ dados_novos (JSON)      │
│ ip_origem               │
│ user_agent              │
│ data_acao               │
└─────────────────────────┘

┌─────────────────────────┐
│    SESSOES_USUARIO      │
├─────────────────────────┤
│ id (PK)                 │
│ usuario_id (FK)         │─────────┐
│ ip_address              │         │ 1:N
│ user_agent              │         │
│ data_criacao            │         │
│ data_expiracao          │         │
│ ativo                   │         │
└─────────────────────────┘         │
                                    │
                                    ▼
                        ┌─────────────────────────┐
                        │        USUARIOS         │
                        │     (referência)        │
                        └─────────────────────────┘
```

## 📋 Legenda dos Relacionamentos

### **Cardinalidades**
- **1:1** - Um para Um
- **1:N** - Um para Muitos  
- **N:M** - Muitos para Muitos

### **Tipos de Chave**
- **(PK)** - Primary Key (Chave Primária)
- **(FK)** - Foreign Key (Chave Estrangeira)
- **(UNIQUE)** - Restrição de Unicidade

### **Relacionamentos Principais**

#### **TRANSPORTADORAS ↔ USUARIOS** (1:N)
- Uma transportadora pode ter múltiplos usuários
- Um usuário pertence a apenas uma transportadora
- Permite gestão hierárquica de acesso

#### **TRANSPORTADORAS ↔ DOCUMENTOS** (1:N)
- Uma transportadora pode ter múltiplos documentos
- Um documento pertence a apenas uma transportadora
- Garante isolamento de dados entre empresas

#### **TIPOS_DOCUMENTO ↔ DOCUMENTOS** (1:N)
- Um tipo pode ser usado por múltiplos documentos
- Um documento tem apenas um tipo
- Permite classificação e padronização

#### **DOCUMENTOS ↔ HISTORICO_DOCUMENTOS** (1:N)
- Um documento pode ter múltiplas entradas de histórico
- Uma entrada de histórico pertence a um documento
- Implementa auditoria completa

#### **USUARIOS ↔ HISTORICO_DOCUMENTOS** (1:N)
- Um usuário pode ter múltiplas ações registradas
- Uma ação é realizada por um usuário
- Rastreabilidade de responsabilidades

#### **USUARIOS ↔ NOTIFICACOES** (1:N)
- Um usuário pode receber múltiplas notificações
- Uma notificação é direcionada a um usuário
- Sistema de comunicação personalizado

#### **USUARIOS ↔ SESSOES_USUARIO** (1:N)
- Um usuário pode ter múltiplas sessões ativas
- Uma sessão pertence a um usuário
- Controle de acesso e segurança

#### **USUARIOS ↔ AUDITORIA_SISTEMA** (1:N)
- Um usuário pode ter múltiplas ações auditadas
- Uma ação de auditoria é realizada por um usuário
- Compliance e rastreabilidade total

## 🔍 Detalhes dos Campos Principais

### **Status de Documento**
```sql
ENUM('pendente', 'aprovado', 'rejeitado', 'vencido', 'renovacao')
```

### **Tipos de Usuário**
```sql
ENUM('admin', 'analista', 'transportadora', 'financeiro')
```

### **Categorias de Documento**
```sql
ENUM('EMPRESA', 'SEGUROS', 'AMBIENTAL', 'FISCAL')
```

### **Status de Cadastro**
```sql
ENUM('PENDENTE', 'APROVADO', 'SUSPENSO', 'INATIVO')
```

### **Classificação de Risco**
```sql
ENUM('BAIXO', 'MEDIO', 'ALTO')
```

### **Canais de Notificação**
```sql
ENUM('email', 'sms', 'push', 'sistema')
```

### **Prioridades de Notificação**
```sql
ENUM('baixa', 'normal', 'alta', 'critica')
```

## 📊 Índices de Performance

### **Índices Primários**
```sql
-- Chaves primárias auto-incrementais
PRIMARY KEY (id) em todas as tabelas

-- Índices únicos
UNIQUE KEY (cnpj) ON transportadoras
UNIQUE KEY (email) ON usuarios  
UNIQUE KEY (numero_protocolo) ON documentos
UNIQUE KEY (chave) ON configuracoes
UNIQUE KEY (codigo) ON tipos_documento
```

### **Índices Secundários Estratégicos**
```sql
-- Performance de consultas frequentes
INDEX idx_documentos_transportadora_status (transportadora_id, status)
INDEX idx_documentos_vencimento_status (data_vencimento, status)
INDEX idx_documentos_tipo_status (tipo_documento_id, status)
INDEX idx_historico_documento_data (documento_id, data_acao)
INDEX idx_notificacoes_usuario_status (usuario_id, status_envio)
INDEX idx_usuarios_transportadora_ativo (transportadora_id, status_ativo)
INDEX idx_auditoria_tabela_registro (tabela_afetada, registro_id)
INDEX idx_sessoes_usuario_ativo (usuario_id, ativo)
```

### **Índices Compostos para Queries Complexas**
```sql
-- Relatórios e dashboards
INDEX idx_documentos_completo (transportadora_id, tipo_documento_id, status, data_upload)
INDEX idx_historico_completo (documento_id, usuario_id, acao, data_acao)
INDEX idx_notificacoes_completo (usuario_id, tipo, status_envio, data_criacao)
```

## 🔒 Constraints e Validações

### **Constraints de Integridade Referencial**
```sql
-- Relacionamentos obrigatórios
FOREIGN KEY (transportadora_id) REFERENCES transportadoras(id) ON DELETE CASCADE
FOREIGN KEY (tipo_documento_id) REFERENCES tipos_documento(id) ON DELETE RESTRICT
FOREIGN KEY (usuario_upload_id) REFERENCES usuarios(id) ON DELETE RESTRICT

-- Relacionamentos opcionais
FOREIGN KEY (usuario_aprovacao_id) REFERENCES usuarios(id) ON DELETE SET NULL
FOREIGN KEY (documento_anterior_id) REFERENCES documentos(id) ON DELETE SET NULL
```

### **Constraints de Validação**
```sql
-- Validações de domínio
CHECK (status IN ('pendente', 'aprovado', 'rejeitado', 'vencido', 'renovacao'))
CHECK (tipo IN ('admin', 'analista', 'transportadora', 'financeiro'))
CHECK (categoria IN ('EMPRESA', 'SEGUROS', 'AMBIENTAL', 'FISCAL'))
CHECK (classificacao_risco IN ('BAIXO', 'MEDIO', 'ALTO'))
CHECK (tamanho_arquivo > 0)
CHECK (valor_garantia >= 0)
CHECK (limite_credito >= 0)
```

### **Triggers de Auditoria**
```sql
-- Trigger para auditoria automática
DELIMITER $$
CREATE TRIGGER tr_documentos_audit 
AFTER UPDATE ON documentos
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_sistema (
        usuario_id, acao, tabela_afetada, registro_id,
        dados_anteriores, dados_novos, data_acao
    ) VALUES (
        @current_user_id, 'UPDATE', 'documentos', NEW.id,
        JSON_OBJECT('status', OLD.status, 'observacoes', OLD.observacoes_analista),
        JSON_OBJECT('status', NEW.status, 'observacoes', NEW.observacoes_analista),
        NOW()
    );
END$$
DELIMITER ;
```

---

**Portal NIMOENERGIA v2.0.0** - Modelo de Entidade-Relacionamento Visual Completo

