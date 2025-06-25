# 🚀 Guia Completo - Portal NIMOENERGIA Local

## 📋 Pré-requisitos

### 🔧 Software Necessário

#### **1. Git**
```bash
# Windows (usando Chocolatey)
choco install git

# macOS (usando Homebrew)
brew install git

# Ubuntu/Debian
sudo apt update && sudo apt install git

# Verificar instalação
git --version
```

#### **2. Python 3.11+**
```bash
# Windows - Baixar de: https://python.org/downloads/
# Marcar "Add Python to PATH" durante instalação

# macOS (usando Homebrew)
brew install python@3.11

# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip

# Verificar instalação
python3 --version
pip3 --version
```

#### **3. Node.js 18+**
```bash
# Windows - Baixar de: https://nodejs.org/

# macOS (usando Homebrew)
brew install node@18

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verificar instalação
node --version
npm --version
```

#### **4. Banco de Dados (Opcional)**

**SQLite (Padrão - Já incluído no Python)**
- ✅ Não requer instalação adicional
- ✅ Ideal para desenvolvimento local
- ✅ Dados armazenados em arquivo local

**MySQL (Opcional)**
```bash
# Windows - Baixar de: https://dev.mysql.com/downloads/installer/

# macOS
brew install mysql
brew services start mysql

# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# Configurar MySQL
sudo mysql_secure_installation
```

**PostgreSQL (Opcional)**
```bash
# Windows - Baixar de: https://www.postgresql.org/download/

# macOS
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

---

## 📥 1. Clonar o Repositório

```bash
# Clonar o projeto
git clone https://github.com/caiopaixao-dev/PortalCadastro.git

# Entrar no diretório
cd PortalCadastro

# Verificar estrutura
ls -la
```

**Estrutura esperada:**
```
PortalCadastro/
├── backend/          # API Flask
├── frontend/         # Interface React
├── database/         # Scripts SQL
├── docs/            # Documentação
├── docker-compose.yml
└── README.md
```

---

## 🐍 2. Configurar Backend (Python/Flask)

### **2.1. Criar Ambiente Virtual**
```bash
# Navegar para backend
cd backend

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Verificar ativação (deve mostrar (venv) no prompt)
which python
```

### **2.2. Instalar Dependências**
```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
pip list | grep Flask
```

### **2.3. Configurar Variáveis de Ambiente**
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar configurações (usar seu editor preferido)
nano .env
# ou
code .env
# ou
notepad .env
```

**Conteúdo do arquivo `.env`:**
```env
# ============================
# CONFIGURAÇÕES DO BANCO DE DADOS
# ============================

# Tipo de banco: sqlite, mysql, postgresql
DATABASE_TYPE=sqlite

# SQLite (Padrão - mais simples)
DATABASE_NAME=portal_nimoenergia.db

# MySQL (Opcional)
# DATABASE_TYPE=mysql
# DATABASE_HOST=localhost
# DATABASE_PORT=3306
# DATABASE_USER=root
# DATABASE_PASSWORD=sua_senha
# DATABASE_NAME=portal_nimoenergia

# PostgreSQL (Opcional)
# DATABASE_TYPE=postgresql
# DATABASE_HOST=localhost
# DATABASE_PORT=5432
# DATABASE_USER=postgres
# DATABASE_PASSWORD=sua_senha
# DATABASE_NAME=portal_nimoenergia

# ============================
# CONFIGURAÇÕES DE SEGURANÇA
# ============================
SECRET_KEY=nimoenergia-local-development-2024
JWT_SECRET_KEY=jwt-local-development-2024

# ============================
# CONFIGURAÇÕES DA APLICAÇÃO
# ============================
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# ============================
# CONFIGURAÇÕES DE CORS
# ============================
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### **2.4. Inicializar Banco de Dados**
```bash
# Executar script de inicialização
python -c "
from database_manager import DatabaseManager
db = DatabaseManager()
db.initialize_database()
print('✅ Banco de dados inicializado com sucesso!')
"
```

### **2.5. Testar Backend**
```bash
# Iniciar servidor de desenvolvimento
python main.py

# Em outro terminal, testar API
curl http://localhost:5000/
curl http://localhost:5000/api/health
```

**Saída esperada:**
```json
{
  "message": "Portal NIMOENERGIA Backend API",
  "version": "2.0.0",
  "status": "online",
  "timestamp": "2024-01-20T10:30:00.000Z"
}
```

---

## ⚛️ 3. Configurar Frontend (React)

### **3.1. Navegar para Frontend**
```bash
# Abrir novo terminal e navegar
cd frontend

# Verificar Node.js
node --version
npm --version
```

### **3.2. Instalar Dependências**
```bash
# Instalar dependências
npm install

# Verificar instalação
npm list react
```

### **3.3. Configurar Variáveis de Ambiente**
```bash
# Criar arquivo de configuração
echo "VITE_API_BASE_URL=http://localhost:5000/api" > .env.local

# Verificar arquivo
cat .env.local
```

### **3.4. Testar Frontend**
```bash
# Iniciar servidor de desenvolvimento
npm run dev

# Acessar no navegador
# http://localhost:3000
```

---

## 🚀 4. Executar Sistema Completo

### **4.1. Método 1: Terminais Separados**

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### **4.2. Método 2: Docker Compose (Recomendado)**
```bash
# Na raiz do projeto
docker-compose up --build

# Para parar
docker-compose down
```

### **4.3. Método 3: Scripts Automatizados**
```bash
# Executar script de setup (será criado na próxima seção)
./scripts/setup.sh

# Executar sistema
./scripts/start.sh
```

---

## 🌐 5. Acessar o Sistema

### **URLs de Acesso:**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **Health Check:** http://localhost:5000/api/health
- **Documentação API:** http://localhost:5000/docs (se disponível)

### **Credenciais de Teste:**
```
Admin NIMOENERGIA:
Email: admin@nimoenergia.com.br
Senha: senha123

Transportadora:
Email: silva@silvatransportes.com.br
Senha: senha123
```

---

## 🧪 6. Executar Testes

### **Backend:**
```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### **Frontend:**
```bash
cd frontend
npm run test
```

---

## 📊 7. Monitoramento e Logs

### **Backend Logs:**
```bash
# Ver logs em tempo real
tail -f backend/logs/app.log

# Verificar status
curl http://localhost:5000/api/health
```

### **Frontend Logs:**
```bash
# Logs aparecem no terminal onde executou npm run dev
# Ou no console do navegador (F12)
```

---

## 🔧 8. Comandos Úteis

### **Reiniciar Serviços:**
```bash
# Backend
cd backend && python main.py

# Frontend
cd frontend && npm run dev

# Docker
docker-compose restart
```

### **Limpar Cache:**
```bash
# Frontend
cd frontend && npm run build

# Backend
cd backend && find . -name "*.pyc" -delete
```

### **Atualizar Dependências:**
```bash
# Backend
cd backend && pip install -r requirements.txt --upgrade

# Frontend
cd frontend && npm update
```

---

## 📱 9. Desenvolvimento

### **Estrutura de Desenvolvimento:**
```
Desenvolvimento Local:
├── Backend: http://localhost:5000
├── Frontend: http://localhost:3000
├── Database: SQLite (arquivo local)
└── Logs: Terminal/Console
```

### **Hot Reload:**
- ✅ **Backend:** Reinicia automaticamente com mudanças
- ✅ **Frontend:** Atualiza automaticamente no navegador
- ✅ **Database:** Mudanças persistem em arquivo local

### **Debugging:**
- **Backend:** Usar debugger Python ou logs
- **Frontend:** Usar DevTools do navegador (F12)
- **API:** Usar Postman ou curl para testar endpoints

---

## ✅ 10. Verificação Final

### **Checklist de Funcionamento:**
- [ ] Backend rodando em http://localhost:5000
- [ ] Frontend rodando em http://localhost:3000
- [ ] API respondendo em /api/health
- [ ] Login funcionando com credenciais de teste
- [ ] Dashboard carregando dados
- [ ] Banco de dados conectado
- [ ] Logs aparecendo nos terminais

### **Teste Completo:**
1. **Acessar:** http://localhost:3000
2. **Fazer login** com: admin@nimoenergia.com.br / senha123
3. **Verificar dashboard** carregando
4. **Testar navegação** entre páginas
5. **Verificar API** em http://localhost:5000/api/health

---

## 🆘 Próximos Passos

Se tudo funcionou:
- ✅ **Sistema rodando localmente**
- ✅ **Pronto para desenvolvimento**
- ✅ **Banco de dados configurado**

Se houver problemas:
- 📖 **Consultar seção de troubleshooting**
- 🔧 **Verificar logs de erro**
- 💬 **Solicitar ajuda com detalhes do erro**

---

**🎉 Parabéns! Seu Portal NIMOENERGIA está rodando localmente!**

