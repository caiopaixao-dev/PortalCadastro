# 🔧 Troubleshooting - Portal NIMOENERGIA

## 🚨 Problemas Comuns e Soluções

### 📋 Índice de Problemas
1. [Problemas de Instalação](#problemas-de-instalação)
2. [Problemas do Backend](#problemas-do-backend)
3. [Problemas do Frontend](#problemas-do-frontend)
4. [Problemas de Banco de Dados](#problemas-de-banco-de-dados)
5. [Problemas de Rede/CORS](#problemas-de-redecors)
6. [Problemas de Performance](#problemas-de-performance)
7. [Problemas de Autenticação](#problemas-de-autenticação)
8. [Problemas do Sistema Operacional](#problemas-do-sistema-operacional)

---

## 🔧 Problemas de Instalação

### ❌ **Erro: "Git não encontrado"**
```bash
# Solução Windows
choco install git
# ou baixar de: https://git-scm.com/

# Solução macOS
brew install git

# Solução Linux
sudo apt update && sudo apt install git
```

### ❌ **Erro: "Python não encontrado"**
```bash
# Verificar se Python está instalado
python3 --version
python --version

# Windows - Baixar de: https://python.org/downloads/
# Marcar "Add Python to PATH"

# macOS
brew install python@3.11

# Linux
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip
```

### ❌ **Erro: "Node.js não encontrado"**
```bash
# Verificar instalação
node --version
npm --version

# Windows - Baixar de: https://nodejs.org/
# macOS
brew install node@18

# Linux
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### ❌ **Erro: "Permission denied" ao executar scripts**
```bash
# Dar permissão de execução
chmod +x setup.sh
chmod +x start.sh
chmod +x check.sh

# Ou para todos os scripts
chmod +x *.sh
```

---

## 🐍 Problemas do Backend

### ❌ **Erro: "ModuleNotFoundError: No module named 'flask'"**
```bash
# Verificar se ambiente virtual está ativado
source backend/venv/bin/activate  # Linux/macOS
backend\venv\Scripts\activate     # Windows

# Reinstalar dependências
pip install -r backend/requirements.txt
```

### ❌ **Erro: "Address already in use" (Porta 5000 ocupada)**
```bash
# Encontrar processo usando a porta
lsof -i :5000          # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Matar processo
kill -9 <PID>          # macOS/Linux
taskkill /PID <PID> /F # Windows

# Ou usar porta diferente
export PORT=5001
python backend/main.py
```

### ❌ **Erro: "Database connection failed"**
```bash
# Verificar arquivo .env
cat backend/.env

# Recriar arquivo .env
cp backend/.env.example backend/.env

# Para SQLite (padrão)
DATABASE_TYPE=sqlite
DATABASE_NAME=portal_nimoenergia.db

# Verificar permissões do diretório
ls -la backend/
```

### ❌ **Erro: "ImportError: No module named 'database_manager'"**
```bash
# Verificar se arquivo existe
ls -la backend/database_manager.py

# Verificar PYTHONPATH
cd backend
export PYTHONPATH=.
python main.py
```

### ❌ **Backend não responde**
```bash
# Verificar se está rodando
curl http://localhost:5000/api/health

# Verificar logs
tail -f backend/logs/app.log

# Reiniciar backend
cd backend
source venv/bin/activate
python main.py
```

---

## ⚛️ Problemas do Frontend

### ❌ **Erro: "npm install failed"**
```bash
# Limpar cache npm
npm cache clean --force

# Deletar node_modules e reinstalar
rm -rf frontend/node_modules
rm frontend/package-lock.json
cd frontend
npm install
```

### ❌ **Erro: "EADDRINUSE: address already in use :::3000"**
```bash
# Encontrar processo na porta 3000
lsof -i :3000          # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Matar processo
kill -9 <PID>          # macOS/Linux
taskkill /PID <PID> /F # Windows

# Ou usar porta diferente
npm run dev -- --port 3001
```

### ❌ **Erro: "Failed to fetch" no navegador**
```bash
# Verificar se backend está rodando
curl http://localhost:5000/api/health

# Verificar arquivo .env.local
cat frontend/.env.local
# Deve conter: VITE_API_BASE_URL=http://localhost:5000/api

# Verificar CORS no backend
# Arquivo backend/.env deve ter:
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### ❌ **Página em branco no navegador**
```bash
# Verificar console do navegador (F12)
# Procurar por erros JavaScript

# Verificar se build está funcionando
cd frontend
npm run build

# Limpar cache do navegador
# Ctrl+Shift+R (hard refresh)
```

### ❌ **Erro: "Module not found" no frontend**
```bash
# Verificar se dependência está instalada
cd frontend
npm list react

# Reinstalar dependências específicas
npm install react react-dom

# Verificar imports no código
# Usar caminhos relativos corretos
```

---

## 🗄️ Problemas de Banco de Dados

### ❌ **Erro: "sqlite3.OperationalError: database is locked"**
```bash
# Fechar todas as conexões
pkill -f python

# Deletar arquivo de lock (se existir)
rm backend/portal_nimoenergia.db-wal
rm backend/portal_nimoenergia.db-shm

# Reiniciar backend
cd backend
source venv/bin/activate
python main.py
```

### ❌ **Erro: "MySQL connection refused"**
```bash
# Verificar se MySQL está rodando
sudo systemctl status mysql    # Linux
brew services list | grep mysql # macOS

# Iniciar MySQL
sudo systemctl start mysql     # Linux
brew services start mysql      # macOS

# Verificar credenciais no .env
DATABASE_TYPE=mysql
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=sua_senha
DATABASE_NAME=portal_nimoenergia
```

### ❌ **Erro: "PostgreSQL connection refused"**
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql    # Linux
brew services list | grep postgresql # macOS

# Iniciar PostgreSQL
sudo systemctl start postgresql     # Linux
brew services start postgresql      # macOS

# Criar banco de dados
sudo -u postgres createdb portal_nimoenergia
```

### ❌ **Banco de dados não inicializa**
```bash
# Executar inicialização manual
cd backend
source venv/bin/activate
python -c "
from database_manager import DatabaseManager
db = DatabaseManager()
db.initialize_database()
"

# Verificar se arquivo de banco foi criado
ls -la *.db
```

---

## 🌐 Problemas de Rede/CORS

### ❌ **Erro: "CORS policy blocked"**
```bash
# Verificar configuração CORS no backend
# Arquivo backend/.env:
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Verificar se Flask-CORS está instalado
cd backend
source venv/bin/activate
pip list | grep Flask-CORS

# Reinstalar se necessário
pip install Flask-CORS
```

### ❌ **Erro: "Network Error" ou "ERR_CONNECTION_REFUSED"**
```bash
# Verificar se backend está rodando
curl http://localhost:5000/api/health

# Verificar firewall
# Windows: Verificar Windows Defender Firewall
# macOS: Verificar System Preferences > Security & Privacy
# Linux: sudo ufw status

# Verificar se porta está aberta
telnet localhost 5000
```

### ❌ **API retorna 404 para todas as rotas**
```bash
# Verificar se está acessando URL correta
curl http://localhost:5000/api/health
# Não: http://localhost:5000/health

# Verificar rotas no backend
cd backend
source venv/bin/activate
python -c "
from main import app
print(app.url_map)
"
```

---

## ⚡ Problemas de Performance

### ❌ **Backend muito lento**
```bash
# Verificar logs de performance
tail -f backend/logs/app.log

# Verificar uso de CPU/memória
top | grep python

# Otimizar banco de dados
# Para SQLite, verificar tamanho do arquivo
ls -lh backend/*.db

# Limpar logs antigos
rm backend/logs/*.log
```

### ❌ **Frontend carrega lentamente**
```bash
# Verificar tamanho do bundle
cd frontend
npm run build
ls -lh dist/

# Limpar cache do navegador
# Ctrl+Shift+Delete

# Verificar network tab no DevTools (F12)
```

### ❌ **Muitas requisições à API**
```bash
# Verificar network tab no navegador (F12)
# Procurar por requisições duplicadas

# Implementar cache no frontend
# Verificar se há loops infinitos
```

---

## 🔐 Problemas de Autenticação

### ❌ **Login não funciona**
```bash
# Verificar credenciais de teste
Email: admin@nimoenergia.com.br
Senha: senha123

# Verificar se API de login responde
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@nimoenergia.com.br","password":"senha123"}'
```

### ❌ **Token JWT inválido**
```bash
# Verificar configuração JWT no .env
JWT_SECRET_KEY=jwt-local-development-2024

# Limpar localStorage no navegador
# F12 > Application > Local Storage > Clear All

# Verificar se token não expirou
# Tokens de teste expiram em 24 horas
```

### ❌ **Redirecionamento após login não funciona**
```bash
# Verificar console do navegador (F12)
# Procurar por erros JavaScript

# Verificar se rotas estão configuradas
# No frontend, verificar React Router
```

---

## 💻 Problemas do Sistema Operacional

### ❌ **Windows: "Scripts execution is disabled"**
```powershell
# Executar PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ou usar Git Bash para executar scripts .sh
```

### ❌ **macOS: "Permission denied" para scripts**
```bash
# Dar permissão de execução
chmod +x *.sh

# Verificar se Xcode Command Line Tools está instalado
xcode-select --install
```

### ❌ **Linux: "sudo: command not found"**
```bash
# Instalar sudo (se necessário)
su -
apt update && apt install sudo

# Adicionar usuário ao grupo sudo
usermod -aG sudo $USER
```

### ❌ **Antivírus bloqueia execução**
```bash
# Windows Defender ou outros antivírus podem bloquear
# Adicionar pasta do projeto às exceções
# Ou temporariamente desabilitar proteção em tempo real
```

---

## 🔍 Comandos de Diagnóstico

### **Verificação Completa do Sistema**
```bash
# Executar script de verificação
./check.sh

# Verificar status dos serviços
ps aux | grep python
ps aux | grep node

# Verificar portas em uso
netstat -tulpn | grep :5000
netstat -tulpn | grep :3000
```

### **Logs e Debug**
```bash
# Backend logs
tail -f backend/logs/app.log

# Frontend logs (no terminal onde executou npm run dev)
# Ou no console do navegador (F12)

# Logs do sistema
# Linux: journalctl -f
# macOS: Console.app
# Windows: Event Viewer
```

### **Teste de Conectividade**
```bash
# Testar backend
curl -v http://localhost:5000/api/health

# Testar frontend
curl -v http://localhost:3000

# Testar conectividade entre frontend e backend
# No console do navegador (F12):
fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(console.log)
```

---

## 🆘 Quando Pedir Ajuda

### **Informações para Incluir:**
1. **Sistema Operacional:** Windows/macOS/Linux + versão
2. **Versões:** Python, Node.js, npm
3. **Erro Exato:** Copiar mensagem de erro completa
4. **Passos Reproduzir:** O que você estava fazendo
5. **Logs:** Saída do terminal/console
6. **Configuração:** Conteúdo dos arquivos .env

### **Comandos para Coletar Informações:**
```bash
# Informações do sistema
uname -a                    # Linux/macOS
systeminfo                 # Windows

# Versões das ferramentas
python3 --version
node --version
npm --version
git --version

# Status do projeto
./check.sh

# Logs recentes
tail -20 backend/logs/app.log
```

---

## ✅ Checklist de Resolução

Antes de pedir ajuda, verifique:

- [ ] Executou `./setup.sh` com sucesso
- [ ] Executou `./check.sh` para verificar sistema
- [ ] Backend está rodando na porta 5000
- [ ] Frontend está rodando na porta 3000
- [ ] Arquivo `.env` existe e está configurado
- [ ] Dependências estão instaladas (venv ativo, node_modules existe)
- [ ] Não há conflitos de porta
- [ ] Firewall/antivírus não está bloqueando
- [ ] Tentou reiniciar os serviços
- [ ] Verificou logs de erro
- [ ] Testou com credenciais corretas

---

**💡 Dica:** A maioria dos problemas é resolvida executando `./setup.sh` novamente!

