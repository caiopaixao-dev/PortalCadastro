#!/bin/bash

# 🚀 Script de Inicialização Rápida - Portal NIMOENERGIA
# Execute este script para iniciar o sistema completo

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
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

# Banner
echo "
🚀 Portal NIMOENERGIA - Inicialização Rápida
==========================================
"

# Verificar se está no diretório correto
if [ ! -f "backend/main.py" ] || [ ! -f "frontend/package.json" ]; then
    print_error "Execute este script na raiz do projeto PortalCadastro!"
    print_info "Estrutura esperada:"
    print_info "  PortalCadastro/"
    print_info "  ├── backend/"
    print_info "  └── frontend/"
    exit 1
fi

# Função para cleanup
cleanup() {
    print_warning "Parando serviços..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    print_success "Serviços parados. Até logo! 👋"
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT SIGTERM

# Verificar dependências
print_info "Verificando dependências..."

# Backend
if [ ! -d "backend/venv" ]; then
    print_error "Ambiente virtual não encontrado!"
    print_info "Execute primeiro: ./setup.sh"
    exit 1
fi

# Frontend
if [ ! -d "frontend/node_modules" ]; then
    print_error "Dependências Node.js não encontradas!"
    print_info "Execute primeiro: ./setup.sh"
    exit 1
fi

print_success "Dependências verificadas!"

# Iniciar Backend
print_info "Iniciando Backend..."
cd backend

# Ativar ambiente virtual e iniciar
source venv/bin/activate
python main.py &
BACKEND_PID=$!

cd ..

# Aguardar backend inicializar
print_info "Aguardando backend inicializar..."
sleep 3

# Verificar se backend está rodando
if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    print_success "Backend iniciado com sucesso! ✅"
else
    print_warning "Backend pode estar iniciando... (normal)"
fi

# Iniciar Frontend
print_info "Iniciando Frontend..."
cd frontend

npm run dev &
FRONTEND_PID=$!

cd ..

# Aguardar frontend inicializar
print_info "Aguardando frontend inicializar..."
sleep 5

# Exibir informações
echo "
🎉 Portal NIMOENERGIA iniciado com sucesso!

📊 Status dos Serviços:
   🐍 Backend:  http://localhost:5000 (PID: $BACKEND_PID)
   ⚛️  Frontend: http://localhost:3000 (PID: $FRONTEND_PID)

🌐 URLs de Acesso:
   🏠 Portal:     http://localhost:3000
   🔧 API:        http://localhost:5000
   ❤️  Health:    http://localhost:5000/api/health

🔑 Credenciais de Teste:
   👨‍💼 Admin NIMOENERGIA:
      Email: admin@nimoenergia.com.br
      Senha: senha123

   🚛 Transportadora:
      Email: silva@silvatransportes.com.br
      Senha: senha123

📝 Comandos Úteis:
   • Parar serviços: Ctrl+C
   • Ver logs: Verifique este terminal
   • Reiniciar: Execute este script novamente

💡 Dicas:
   • Mudanças no código são aplicadas automaticamente
   • Use F12 no navegador para debug do frontend
   • Logs do backend aparecem neste terminal
   • Para desenvolvimento, mantenha este terminal aberto

🔄 Aguardando... (Pressione Ctrl+C para parar)
"

# Aguardar indefinidamente
while true; do
    # Verificar se processos ainda estão rodando
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        print_error "Backend parou inesperadamente!"
        break
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        print_error "Frontend parou inesperadamente!"
        break
    fi
    
    sleep 5
done

cleanup

