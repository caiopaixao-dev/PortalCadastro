# Documentação Técnica Avançada - Portal NIMOENERGIA

## 🏗️ Arquitetura do Sistema

### Visão Geral da Arquitetura

O Portal NIMOENERGIA foi desenvolvido seguindo os princípios de **Clean Architecture** e **Domain-Driven Design (DDD)**, garantindo separação clara de responsabilidades, testabilidade e manutenibilidade do código.

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITETURA PORTAL NIMOENERGIA              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  Frontend   │    │   Backend   │    │  Database   │         │
│  │   React     │◄──►│    Flask    │◄──►│   MySQL/    │         │
│  │ Tailwind CSS│    │   Python    │    │ PostgreSQL/ │         │
│  │    PWA      │    │     API     │    │   SQLite    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Nginx     │    │    Redis    │    │   Storage   │         │
│  │   Proxy     │    │    Cache    │    │    Files    │         │
│  │    SSL      │    │Rate Limiting│    │   Backup    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Camadas da Aplicação

#### 1. **Camada de Apresentação (Frontend)**
- **Framework**: React 18 com hooks modernos
- **Styling**: Tailwind CSS para design system consistente
- **Estado**: Context API + useReducer para gerenciamento global
- **Roteamento**: React Router v6 com lazy loading
- **Build**: Vite para desenvolvimento rápido e build otimizado
- **PWA**: Service Workers para funcionalidade offline

#### 2. **Camada de API (Backend)**
- **Framework**: Flask 3.0 com blueprints modulares
- **Autenticação**: JWT com refresh tokens
- **Validação**: Marshmallow para serialização/deserialização
- **ORM**: SQLAlchemy (opcional) ou queries nativas otimizadas
- **Cache**: Redis para sessões e rate limiting
- **Logs**: Structured logging com correlação de requests

#### 3. **Camada de Dados (Database)**
- **SGBD Principal**: MySQL 8.0 para produção
- **SGBD Alternativo**: PostgreSQL para Heroku
- **SGBD Desenvolvimento**: SQLite para ambiente local
- **Migrations**: Scripts SQL versionados
- **Backup**: Automated daily backups com retenção de 30 dias

## 🔐 Segurança e Compliance

### Implementações de Segurança

#### **Autenticação e Autorização**
```python
# JWT com claims customizados
{
  "user_id": 123,
  "email": "user@example.com",
  "role": "transportadora",
  "permissions": ["read:documents", "write:documents"],
  "transportadora_id": 456,
  "exp": 1640995200,
  "iat": 1640908800,
  "jti": "unique-token-id"
}
```

#### **Rate Limiting Avançado**
- **Global**: 1000 requests/hour por IP
- **Login**: 10 tentativas/minuto por IP
- **Upload**: 5 uploads/minuto por usuário
- **API**: 100 requests/minuto por token

#### **Validação de Entrada**
```python
# Exemplo de validação robusta
class DocumentoSchema(Schema):
    tipo_documento_id = fields.Integer(required=True, validate=validate.Range(min=1))
    arquivo = fields.Raw(required=True, validate=validate_file)
    data_vencimento = fields.Date(allow_none=True)
    valor_garantia = fields.Decimal(places=2, allow_none=True)
    
    @validates('arquivo')
    def validate_file(self, value):
        if not value:
            raise ValidationError('Arquivo é obrigatório')
        if value.content_length > 50 * 1024 * 1024:  # 50MB
            raise ValidationError('Arquivo muito grande')
        if not value.filename.lower().endswith(('.pdf', '.doc', '.docx')):
            raise ValidationError('Formato não permitido')
```

#### **Headers de Segurança**
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
```

## 📊 Performance e Otimização

### Estratégias de Performance

#### **Database Optimization**
```sql
-- Índices estratégicos para queries frequentes
CREATE INDEX idx_documentos_transportadora_status ON documentos(transportadora_id, status);
CREATE INDEX idx_documentos_vencimento_status ON documentos(data_vencimento, status);
CREATE INDEX idx_historico_documento_data ON historico_documentos(documento_id, data_acao);

-- Particionamento para tabelas grandes
ALTER TABLE historico_documentos 
PARTITION BY RANGE (YEAR(data_acao)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

#### **Caching Strategy**
```python
# Cache de queries frequentes
@cache.memoize(timeout=300)  # 5 minutos
def get_tipos_documento():
    return db.session.query(TipoDocumento).filter_by(ativo=True).all()

# Cache de sessões
@cache.memoize(timeout=3600)  # 1 hora
def get_user_permissions(user_id):
    return db.session.query(User).get(user_id).permissions
```

#### **Frontend Optimization**
```javascript
// Code splitting por rota
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Documentos = lazy(() => import('./pages/Documentos'));

// Memoização de componentes pesados
const DocumentList = memo(({ documents, onUpdate }) => {
  return documents.map(doc => <DocumentCard key={doc.id} document={doc} />);
});

// Debounce para pesquisas
const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  
  return debouncedValue;
};
```

## 🧪 Testes e Qualidade

### Estratégia de Testes

#### **Backend Testing**
```python
# Testes unitários
class TestDocumentoService(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def test_upload_documento_valido(self):
        with self.app.test_client() as client:
            response = client.post('/api/documentos', 
                data={'tipo_documento_id': 1, 'arquivo': (io.BytesIO(b'test'), 'test.pdf')},
                headers={'Authorization': f'Bearer {self.get_token()}'})
            self.assertEqual(response.status_code, 201)

# Testes de integração
class TestDocumentoAPI(APITestCase):
    def test_workflow_completo_documento(self):
        # 1. Upload
        # 2. Aprovação
        # 3. Notificação
        # 4. Histórico
        pass
```

#### **Frontend Testing**
```javascript
// Testes de componentes
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from './LoginForm';

test('deve exibir erro para credenciais inválidas', async () => {
  render(<LoginForm />);
  
  fireEvent.change(screen.getByLabelText(/email/i), {
    target: { value: 'invalid@email.com' }
  });
  fireEvent.change(screen.getByLabelText(/senha/i), {
    target: { value: 'wrongpassword' }
  });
  fireEvent.click(screen.getByRole('button', { name: /entrar/i }));
  
  expect(await screen.findByText(/credenciais inválidas/i)).toBeInTheDocument();
});

// Testes E2E com Playwright
test('fluxo completo de upload de documento', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid=email]', 'user@test.com');
  await page.fill('[data-testid=password]', 'password123');
  await page.click('[data-testid=login-button]');
  
  await page.goto('/documentos');
  await page.setInputFiles('[data-testid=file-input]', 'test-document.pdf');
  await page.selectOption('[data-testid=tipo-documento]', '1');
  await page.click('[data-testid=upload-button]');
  
  await expect(page.locator('[data-testid=success-message]')).toBeVisible();
});
```

## 🚀 Deploy e DevOps

### Pipeline CI/CD

```yaml
# .github/workflows/deploy.yml
name: Deploy Portal NIMOENERGIA

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          cd backend
          pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: |
          docker build -t portal-nimoenergia .
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push portal-nimoenergia:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "portal-nimoenergia"
          heroku_email: "deploy@nimoenergia.com"
```

### Monitoramento e Observabilidade

#### **Métricas de Aplicação**
```python
from prometheus_client import Counter, Histogram, generate_latest

# Métricas customizadas
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint,
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.observe(time.time() - g.start_time)
    return response

@app.route('/metrics')
def metrics():
    return generate_latest()
```

#### **Health Checks Avançados**
```python
@app.route('/api/health/detailed')
def health_detailed():
    checks = {
        'database': check_database_connection(),
        'redis': check_redis_connection(),
        'storage': check_storage_availability(),
        'external_apis': check_external_dependencies()
    }
    
    overall_status = 'healthy' if all(checks.values()) else 'degraded'
    
    return jsonify({
        'status': overall_status,
        'timestamp': datetime.utcnow().isoformat(),
        'checks': checks,
        'version': app.config['VERSION'],
        'uptime': get_uptime()
    })
```

## 📈 Escalabilidade e Futuro

### Roadmap Técnico

#### **Fase 1 - Fundação (Atual)**
- ✅ Arquitetura base implementada
- ✅ CRUD completo de documentos
- ✅ Sistema de autenticação robusto
- ✅ Interface responsiva

#### **Fase 2 - Otimização (Q1 2024)**
- 🔄 Implementação de cache distribuído
- 🔄 Otimização de queries complexas
- 🔄 Implementação de CDN
- 🔄 Monitoramento avançado

#### **Fase 3 - Inteligência (Q2 2024)**
- 📋 OCR para extração automática de dados
- 📋 Machine Learning para validação de documentos
- 📋 Análise preditiva de compliance
- 📋 Chatbot para suporte automatizado

#### **Fase 4 - Integração (Q3 2024)**
- 📋 APIs para sistemas externos
- 📋 Integração com órgãos reguladores
- 📋 Blockchain para auditoria imutável
- 📋 Mobile app nativo

### Considerações de Escalabilidade

#### **Horizontal Scaling**
```yaml
# kubernetes/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portal-nimoenergia
spec:
  replicas: 3
  selector:
    matchLabels:
      app: portal-nimoenergia
  template:
    metadata:
      labels:
        app: portal-nimoenergia
    spec:
      containers:
      - name: app
        image: portal-nimoenergia:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

#### **Database Sharding Strategy**
```sql
-- Sharding por transportadora_id
CREATE TABLE documentos_shard_1 (
    LIKE documentos INCLUDING ALL
) INHERITS (documentos);

CREATE TABLE documentos_shard_2 (
    LIKE documentos INCLUDING ALL
) INHERITS (documentos);

-- Constraint para direcionamento automático
ALTER TABLE documentos_shard_1 ADD CONSTRAINT shard_1_check 
CHECK (transportadora_id % 2 = 1);

ALTER TABLE documentos_shard_2 ADD CONSTRAINT shard_2_check 
CHECK (transportadora_id % 2 = 0);
```

---

**Portal NIMOENERGIA v2.0.0** - Documentação Técnica Avançada

