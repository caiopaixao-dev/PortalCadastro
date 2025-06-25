#!/bin/bash

# 🔍 Script de Verificação - Portal NIMOENERGIA
# Verifica se o sistema está funcionando corretamente

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
    echo -e "${GREEN}[✅ PASS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️  WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌ FAIL]${NC} $1"
}

# Contador de testes
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_WARNED=0

# Função para executar teste
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"
    
    print_info "Testando: $test_name"
    
    if eval "$test_command" > /dev/null 2>&1; then
        print_success "$test_name"
        ((TESTS_PASSED++))
        return 0
    else
        if [ "$expected_result" = "warning" ]; then
            print_warning "$test_name (não crítico)"
            ((TESTS_WARNED++))
            return 1
        else
            print_error "$test_name"
            ((TESTS_FAILED++))
            return 1
        fi
    fi
}

# Banner
echo "
🔍 Portal NIMOENERGIA - Verificação do Sistema
============================================
"

print_info "Iniciando verificação completa..."

# 1. Verificar estrutura de arquivos
print_info "📁 Verificando estrutura de arquivos..."

run_test "Diretório backend existe" "[ -d 'backend' ]"
run_test "Diretório frontend existe" "[ -d 'frontend' ]"
run_test "Arquivo main.py existe" "[ -f 'backend/main.py' ]"
run_test "Arquivo package.json existe" "[ -f 'frontend/package.json' ]"
run_test "Arquivo requirements.txt existe" "[ -f 'backend/requirements.txt' ]"

# 2. Verificar dependências do sistema
print_info "🔧 Verificando dependências do sistema..."

run_test "Git instalado" "command -v git"
run_test "Python 3 instalado" "command -v python3"
run_test "Node.js instalado" "command -v node"
run_test "npm instalado" "command -v npm"

# 3. Verificar ambiente Python
print_info "🐍 Verificando ambiente Python..."

run_test "Ambiente virtual existe" "[ -d 'backend/venv' ]"

if [ -d "backend/venv" ]; then
    cd backend
    source venv/bin/activate
    
    run_test "Flask instalado" "python -c 'import flask'"
    run_test "Flask-CORS instalado" "python -c 'import flask_cors'"
    run_test "PyJWT instalado" "python -c 'import jwt'"
    run_test "bcrypt instalado" "python -c 'import bcrypt'"
    run_test "python-dotenv instalado" "python -c 'import dotenv'"
    
    # Testar importação do main
    run_test "main.py importável" "python -c 'import main'"
    
    cd ..
else
    print_error "Ambiente virtual não encontrado - pulando testes Python"
    ((TESTS_FAILED += 5))
fi

# 4. Verificar ambiente Node.js
print_info "⚛️ Verificando ambiente Node.js..."

run_test "node_modules existe" "[ -d 'frontend/node_modules' ]"

if [ -d "frontend/node_modules" ]; then
    cd frontend
    
    run_test "React instalado" "npm list react --depth=0"
    run_test "Vite instalado" "npm list vite --depth=0"
    run_test "Vitest instalado" "npm list vitest --depth=0" "warning"
    
    cd ..
else
    print_error "node_modules não encontrado - pulando testes Node.js"
    ((TESTS_FAILED += 3))
fi

# 5. Verificar configurações
print_info "⚙️ Verificando configurações..."

run_test "Arquivo .env backend existe" "[ -f 'backend/.env' ]"
run_test "Arquivo .env.local frontend existe" "[ -f 'frontend/.env.local' ]" "warning"

# 6. Verificar serviços (se estiverem rodando)
print_info "🌐 Verificando serviços..."

run_test "Backend respondendo" "curl -s http://localhost:5000/api/health" "warning"
run_test "Frontend acessível" "curl -s http://localhost:3000" "warning"

# 7. Verificar banco de dados
print_info "🗄️ Verificando banco de dados..."

if [ -f "backend/.env" ]; then
    cd backend
    if [ -d "venv" ]; then
        source venv/bin/activate
        run_test "Conexão com banco" "python -c '
from database_manager import DatabaseManager
db = DatabaseManager()
conn = db.get_connection()
if conn: 
    conn.close()
    print(\"OK\")
else: 
    raise Exception(\"No connection\")
'" "warning"
    fi
    cd ..
fi

# 8. Verificar scripts
print_info "📜 Verificando scripts..."

run_test "Script setup.sh existe" "[ -f 'setup.sh' ]" "warning"
run_test "Script start.sh existe" "[ -f 'start.sh' ]" "warning"

# 9. Verificar permissões
print_info "🔐 Verificando permissões..."

run_test "Backend/main.py legível" "[ -r 'backend/main.py' ]"
run_test "Frontend/package.json legível" "[ -r 'frontend/package.json' ]"

# 10. Testes funcionais básicos
print_info "🧪 Executando testes funcionais..."

# Teste de importação Python
if [ -d "backend/venv" ]; then
    cd backend
    source venv/bin/activate
    
    run_test "Teste de importação Flask" "python -c '
from flask import Flask
app = Flask(__name__)
print(\"OK\")
'"
    
    run_test "Teste de configuração" "python -c '
import os
from dotenv import load_dotenv
load_dotenv()
print(\"OK\")
'"
    
    cd ..
fi

# Teste de build frontend
if [ -d "frontend/node_modules" ]; then
    cd frontend
    run_test "Build frontend" "npm run build" "warning"
    cd ..
fi

# Relatório final
echo "
📊 RELATÓRIO DE VERIFICAÇÃO
==========================

✅ Testes Passaram: $TESTS_PASSED
⚠️  Avisos: $TESTS_WARNED  
❌ Testes Falharam: $TESTS_FAILED

"

if [ $TESTS_FAILED -eq 0 ]; then
    print_success "🎉 Sistema verificado com sucesso!"
    print_info "✅ Pronto para execução!"
    
    if [ $TESTS_WARNED -gt 0 ]; then
        print_warning "⚠️  Alguns avisos foram encontrados, mas não são críticos."
    fi
    
    echo "
🚀 Próximos passos:
   1. Execute: ./start.sh
   2. Acesse: http://localhost:3000
   3. Faça login com: admin@nimoenergia.com.br / senha123
"
    
elif [ $TESTS_FAILED -le 3 ]; then
    print_warning "⚠️  Sistema com problemas menores"
    print_info "Alguns testes falharam, mas o sistema pode funcionar."
    print_info "Execute ./setup.sh para corrigir problemas de configuração."
    
else
    print_error "❌ Sistema com problemas críticos"
    print_info "Muitos testes falharam. Execute ./setup.sh para configurar o ambiente."
fi

echo "
📖 Para mais informações:
   • Consulte o GUIA_INSTALACAO_LOCAL.md
   • Execute ./setup.sh para configuração automática
   • Verifique os logs de erro acima
"

