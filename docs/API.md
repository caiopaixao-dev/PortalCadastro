# API Documentation - Portal NIMOENERGIA

## 📋 Visão Geral

A API do Portal NIMOENERGIA é uma API RESTful robusta e segura, desenvolvida com Flask e projetada para escalabilidade e performance.

## 🔗 Base URL

```
Desenvolvimento: http://localhost:5000/api
Produção: https://portal-nimoenergia.herokuapp.com/api
```

## 🔐 Autenticação

A API utiliza autenticação JWT (JSON Web Tokens) para proteger endpoints.

### Obter Token
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```

**Resposta de Sucesso:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@exemplo.com",
    "tipo": "transportadora",
    "transportadora_id": 5,
    "transportadora_nome": "Silva Transportes"
  }
}
```

### Usar Token
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📊 Endpoints

### 🏠 Sistema

#### Status da API
```http
GET /
```

**Resposta:**
```json
{
  "message": "Portal NIMOENERGIA Backend API",
  "version": "2.0.0",
  "status": "online",
  "database": "mysql",
  "timestamp": "2024-01-01T00:00:00Z",
  "endpoints": {
    "auth": "/api/auth/login",
    "users": "/api/users",
    "transportadoras": "/api/transportadoras",
    "documentos": "/api/documentos",
    "dashboard": "/api/dashboard",
    "health": "/api/health"
  }
}
```

#### Health Check
```http
GET /api/health
```

**Resposta:**
```json
{
  "status": "healthy",
  "database": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "uptime": "72h 15m 30s"
}
```

### 🔐 Autenticação

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@nimoenergia.com.br",
  "password": "admin123"
}
```

**Rate Limit:** 10 requests/minute

**Respostas:**
- `200` - Login realizado com sucesso
- `401` - Credenciais inválidas
- `429` - Muitas tentativas

### 👥 Usuários

#### Criar Usuário
```http
POST /api/users
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@exemplo.com",
  "password": "senha123",
  "tipo": "transportadora",
  "transportadora_id": 5
}
```

**Rate Limit:** 5 requests/minute

**Validações:**
- Email deve ser válido e único
- Senha deve ter pelo menos 8 caracteres
- Tipo deve ser: `admin`, `analista`, `transportadora`, `financeiro`

**Respostas:**
- `201` - Usuário criado com sucesso
- `400` - Dados inválidos
- `409` - Email já existe

#### Listar Usuários (Admin)
```http
GET /api/users
Authorization: Bearer {token}
```

**Permissão:** Apenas administradores

### 🚛 Transportadoras

#### Criar Transportadora
```http
POST /api/transportadoras
Authorization: Bearer {token}
Content-Type: application/json

{
  "cnpj": "12.345.678/0001-90",
  "nome": "Silva Transportes Ltda",
  "email": "contato@silvatransportes.com",
  "telefone": "(11) 99999-9999",
  "endereco": "Rua das Flores, 123 - São Paulo/SP"
}
```

**Validações:**
- CNPJ deve ser válido e único
- Nome é obrigatório

**Respostas:**
- `201` - Transportadora criada
- `400` - Dados inválidos
- `409` - CNPJ já existe

#### Listar Transportadoras (Admin)
```http
GET /api/transportadoras
Authorization: Bearer {token}
```

**Permissão:** Apenas administradores

**Resposta:**
```json
[
  {
    "id": 1,
    "cnpj": "12.345.678/0001-90",
    "nome": "Silva Transportes Ltda",
    "email": "contato@silvatransportes.com",
    "telefone": "(11) 99999-9999",
    "endereco": "Rua das Flores, 123 - São Paulo/SP",
    "ativo": true,
    "data_cadastro": "2024-01-01T00:00:00Z"
  }
]
```

### 📄 Documentos

#### Upload de Documento
```http
POST /api/documentos
Authorization: Bearer {token}
Content-Type: multipart/form-data

{
  "tipo_documento_id": 1,
  "arquivo": [file],
  "data_vencimento": "2024-12-31",
  "valor_garantia": 50000.00,
  "observacoes": "Documento renovado"
}
```

**Validações:**
- Arquivo deve ser PDF, DOC, DOCX, JPG, PNG
- Tamanho máximo: 50MB
- Tipo de documento deve existir

**Respostas:**
- `201` - Documento enviado
- `400` - Arquivo inválido
- `413` - Arquivo muito grande

#### Listar Documentos
```http
GET /api/documentos?status=pendente&tipo=1&page=1&limit=20
Authorization: Bearer {token}
```

**Parâmetros de Query:**
- `status`: `pendente`, `aprovado`, `rejeitado`, `vencido`
- `tipo`: ID do tipo de documento
- `transportadora_id`: ID da transportadora (admin only)
- `page`: Página (padrão: 1)
- `limit`: Itens por página (padrão: 20, máximo: 100)

**Resposta:**
```json
{
  "documentos": [
    {
      "id": 1,
      "numero_protocolo": "DOC-2024-001",
      "transportadora_nome": "Silva Transportes",
      "tipo_documento_nome": "Seguro RC",
      "nome_arquivo_original": "seguro_rc_2024.pdf",
      "data_upload": "2024-01-01T10:00:00Z",
      "data_vencimento": "2024-12-31",
      "status": "pendente",
      "valor_garantia": 50000.00
    }
  ],
  "total": 150,
  "page": 1,
  "pages": 8,
  "per_page": 20
}
```

#### Aprovar/Rejeitar Documento (Admin/Analista)
```http
PUT /api/documentos/{id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "aprovado",
  "observacoes": "Documento aprovado conforme análise"
}
```

**Status válidos:** `aprovado`, `rejeitado`

### 📊 Dashboard

#### Dados do Dashboard
```http
GET /api/dashboard
Authorization: Bearer {token}
```

**Resposta (Admin):**
```json
{
  "total_transportadoras": 25,
  "total_usuarios": 50,
  "total_documentos": 1250,
  "documentos_pendentes": 15,
  "documentos_vencendo": 8,
  "compliance_medio": 85.5
}
```

**Resposta (Transportadora):**
```json
{
  "meus_documentos": 45,
  "documentos_pendentes": 3,
  "documentos_aprovados": 40,
  "documentos_vencendo": 2,
  "compliance_percentual": 88.9
}
```

### 📋 Tipos de Documento

#### Listar Tipos
```http
GET /api/tipos-documentos
```

**Resposta:**
```json
[
  {
    "id": 1,
    "codigo": "SEGURO_RC",
    "nome": "Seguro de Responsabilidade Civil",
    "categoria": "SEGUROS",
    "obrigatorio": true,
    "tem_vencimento": true,
    "tem_garantia": true,
    "ativo": true
  }
]
```

## 🔒 Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Requisição bem-sucedida |
| 201 | Created - Recurso criado com sucesso |
| 400 | Bad Request - Dados inválidos |
| 401 | Unauthorized - Token inválido ou ausente |
| 403 | Forbidden - Sem permissão para acessar |
| 404 | Not Found - Recurso não encontrado |
| 409 | Conflict - Recurso já existe |
| 413 | Payload Too Large - Arquivo muito grande |
| 422 | Unprocessable Entity - Dados não processáveis |
| 429 | Too Many Requests - Rate limit excedido |
| 500 | Internal Server Error - Erro interno |

## 🚨 Tratamento de Erros

### Formato Padrão de Erro
```json
{
  "error": "Mensagem de erro descritiva",
  "code": "ERROR_CODE",
  "details": {
    "field": "Campo específico com erro",
    "message": "Detalhes do erro"
  },
  "timestamp": "2024-01-01T00:00:00Z",
  "request_id": "uuid-da-requisicao"
}
```

### Exemplos de Erros

#### Validação de Dados
```json
{
  "error": "Dados de entrada inválidos",
  "code": "VALIDATION_ERROR",
  "details": {
    "email": "Email deve ter formato válido",
    "password": "Senha deve ter pelo menos 8 caracteres"
  }
}
```

#### Rate Limit
```json
{
  "error": "Muitas requisições. Tente novamente em 60 segundos.",
  "code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 60
}
```

#### Token Inválido
```json
{
  "error": "Token expirado",
  "code": "TOKEN_EXPIRED"
}
```

## 🔄 Rate Limiting

### Limites por Endpoint

| Endpoint | Limite |
|----------|--------|
| Global | 1000/hora, 100/minuto |
| `/api/auth/login` | 10/minuto |
| `/api/users` (POST) | 5/minuto |
| `/api/documentos` (POST) | 10/minuto |

### Headers de Rate Limit
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## 📝 Logs e Auditoria

### Logs de Requisição
Todas as requisições são logadas com:
- Request ID único
- IP do cliente
- User Agent
- Timestamp
- Duração da requisição
- Status de resposta

### Auditoria de Ações
Ações críticas são auditadas:
- Login/logout de usuários
- Criação/edição de recursos
- Aprovação/rejeição de documentos
- Mudanças de status

## 🧪 Testando a API

### cURL Examples

#### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@nimoenergia.com.br","password":"admin123"}'
```

#### Listar Documentos
```bash
curl -X GET http://localhost:5000/api/documentos \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Upload de Documento
```bash
curl -X POST http://localhost:5000/api/documentos \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "tipo_documento_id=1" \
  -F "arquivo=@documento.pdf" \
  -F "data_vencimento=2024-12-31"
```

### Postman Collection
Importe a collection do Postman disponível em `/docs/postman_collection.json`

## 🔧 Configuração de Desenvolvimento

### Variáveis de Ambiente
```bash
# API Configuration
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=dev-secret-key
JWT_SECRET_KEY=dev-jwt-secret

# Database
DATABASE_TYPE=sqlite
DATABASE_PATH=dev_portal.db

# Logging
LOG_LEVEL=DEBUG
LOG_TO_CONSOLE=true
```

### Executar em Modo Debug
```bash
export FLASK_ENV=development
export FLASK_DEBUG=true
python main.py
```

## 📚 SDKs e Bibliotecas

### JavaScript/TypeScript
```javascript
// Exemplo de uso com fetch
const api = {
  baseURL: 'http://localhost:5000/api',
  token: localStorage.getItem('token'),
  
  async request(endpoint, options = {}) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { Authorization: `Bearer ${this.token}` }),
        ...options.headers
      },
      ...options
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    return response.json();
  },
  
  async login(email, password) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    
    this.token = response.token;
    localStorage.setItem('token', response.token);
    return response;
  }
};
```

### Python
```python
import requests

class NimoAPI:
    def __init__(self, base_url='http://localhost:5000/api'):
        self.base_url = base_url
        self.token = None
    
    def login(self, email, password):
        response = requests.post(f'{self.base_url}/auth/login', json={
            'email': email,
            'password': password
        })
        response.raise_for_status()
        data = response.json()
        self.token = data['token']
        return data
    
    def get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def get_dashboard(self):
        response = requests.get(
            f'{self.base_url}/dashboard',
            headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()
```

---

**Portal NIMOENERGIA API v2.0.0** - Documentação completa da API RESTful

