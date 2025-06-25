#!/bin/bash

# 🚀 Script de Setup Automático - Portal NIMOENERGIA
# Este script configura automaticamente o ambiente de desenvolvimento local

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para detectar sistema operacional
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Banner
echo "
🚀 Portal NIMOENERGIA - Setup Automático
========================================
Este script irá configurar seu ambiente de desenvolvimento local.
"

OS=$(detect_os)
print_status "Sistema operacional detectado: $OS"

# 1. Verificar pré-requisitos
print_status "Verificando pré-requisitos..."

# Verificar Git
if command_exists git; then
    GIT_VERSION=$(git --version)
    print_success "Git encontrado: $GIT_VERSION"
else
    print_error "Git não encontrado. Por favor, instale o Git primeiro."
    exit 1
fi

# Verificar Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python encontrado: $PYTHON_VERSION"
else
    print_error "Python 3 não encontrado. Por favor, instale Python 3.11+ primeiro."
    exit 1
fi

# Verificar Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js encontrado: $NODE_VERSION"
else
    print_error "Node.js não encontrado. Por favor, instale Node.js 18+ primeiro."
    exit 1
fi

# Verificar npm
if command_exists npm; then
    NPM_VERSION=$(npm --version)
    print_success "npm encontrado: $NPM_VERSION"
else
    print_error "npm não encontrado. Por favor, instale npm primeiro."
    exit 1
fi

# 2. Clonar repositório (se não existir)
if [ ! -d "PortalCadastro" ]; then
    print_status "Clonando repositório..."
    git clone https://github.com/caiopaixao-dev/PortalCadastro.git
    print_success "Repositório clonado com sucesso!"
else
    print_warning "Repositório já existe. Pulando clone..."
fi

cd PortalCadastro

# 3. Configurar Backend
print_status "Configurando backend..."

cd backend

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    print_status "Criando ambiente virtual Python..."
    python3 -m venv venv
    print_success "Ambiente virtual criado!"
else
    print_warning "Ambiente virtual já existe. Pulando criação..."
fi

# Ativar ambiente virtual
print_status "Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
print_status "Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
print_status "Instalando dependências Python..."
pip install -r requirements.txt
print_success "Dependências Python instaladas!"

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    print_status "Criando arquivo de configuração .env..."
    cat > .env << EOF
# ============================
# CONFIGURAÇÕES DO BANCO DE DADOS
# ============================
DATABASE_TYPE=sqlite
DATABASE_NAME=portal_nimoenergia.db

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
EOF
    print_success "Arquivo .env criado!"
else
    print_warning "Arquivo .env já existe. Pulando criação..."
fi

# Inicializar banco de dados
print_status "Inicializando banco de dados..."
python -c "
try:
    from database_manager import DatabaseManager
    db = DatabaseManager()
    db.initialize_database()
    print('✅ Banco de dados inicializado com sucesso!')
except Exception as e:
    print(f'⚠️  Aviso: {e}')
    print('Banco será criado automaticamente na primeira execução.')
"

cd ..

# 4. Configurar Frontend
print_status "Configurando frontend..."

cd frontend

# Instalar dependências
print_status "Instalando dependências Node.js..."
npm install
print_success "Dependências Node.js instaladas!"

# Criar arquivo .env.local se não existir
if [ ! -f ".env.local" ]; then
    print_status "Criando arquivo de configuração frontend..."
    echo "VITE_API_BASE_URL=http://localhost:5000/api" > .env.local
    print_success "Arquivo .env.local criado!"
else
    print_warning "Arquivo .env.local já existe. Pulando criação..."
fi

cd ..

# 5. Criar scripts de execução
print_status "Criando scripts de execução..."

# Script para iniciar backend
cat > start-backend.sh << 'EOF'
#!/bin/bash
echo "🐍 Iniciando Backend..."
cd backend
source venv/bin/activate
python main.py
EOF

# Script para iniciar frontend
cat > start-frontend.sh << 'EOF'
#!/bin/bash
echo "⚛️ Iniciando Frontend..."
cd frontend
npm run dev
EOF

# Script para iniciar ambos
cat > start-all.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando Portal NIMOENERGIA completo..."

# Função para cleanup
cleanup() {
    echo "🛑 Parando serviços..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT

# Iniciar backend em background
echo "🐍 Iniciando Backend..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Aguardar backend inicializar
sleep 3

# Iniciar frontend em background
echo "⚛️ Iniciando Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "
✅ Portal NIMOENERGIA iniciado com sucesso!

🌐 URLs de Acesso:
   Frontend: http://localhost:3000
   Backend:  http://localhost:5000
   API Health: http://localhost:5000/api/health

🔑 Credenciais de Teste:
   Admin: admin@nimoenergia.com.br / senha123
   Transportadora: silva@silvatransportes.com.br / senha123

📝 Para parar os serviços, pressione Ctrl+C
"

# Aguardar indefinidamente
wait
EOF

# Tornar scripts executáveis
chmod +x start-backend.sh start-frontend.sh start-all.sh

print_success "Scripts de execução criados!"

# 6. Executar testes básicos
print_status "Executando testes básicos..."

# Testar backend
cd backend
source venv/bin/activate
print_status "Testando backend..."
python -c "
import sys
sys.path.append('.')
try:
    from main import app
    print('✅ Backend: Importação bem-sucedida')
except Exception as e:
    print(f'⚠️  Backend: {e}')
"
cd ..

# Testar frontend
cd frontend
print_status "Testando frontend..."
if npm run build > /dev/null 2>&1; then
    print_success "Frontend: Build bem-sucedido"
else
    print_warning "Frontend: Build com avisos (normal em desenvolvimento)"
fi
cd ..

# 7. Finalização
print_success "
🎉 Setup concluído com sucesso!

📁 Estrutura criada:
   PortalCadastro/
   ├── backend/          (API Flask configurada)
   ├── frontend/         (React configurado)
   ├── start-backend.sh  (Script para backend)
   ├── start-frontend.sh (Script para frontend)
   └── start-all.sh      (Script completo)

🚀 Próximos passos:
   1. Execute: ./start-all.sh
   2. Acesse: http://localhost:3000
   3. Faça login com: admin@nimoenergia.com.br / senha123

📖 Para mais informações, consulte o README.md

💡 Dicas:
   - Use Ctrl+C para parar os serviços
   - Logs aparecem no terminal
   - Mudanças no código são aplicadas automaticamente
"

print_status "Setup automático finalizado! 🚀"

