# ⚡ Guia Rápido - Portal NIMOENERGIA Local

## 🚀 Início Rápido (5 minutos)

### **Pré-requisitos Mínimos:**
- ✅ Git instalado
- ✅ Python 3.11+ instalado  
- ✅ Node.js 18+ instalado

### **Passos Rápidos:**

#### **1. Clonar e Configurar (2 min)**
```bash
# Clonar repositório
git clone https://github.com/caiopaixao-dev/PortalCadastro.git
cd PortalCadastro

# Executar setup automático
chmod +x scripts/setup.sh
./scripts/setup.sh
``` 

#### **2. Iniciar Sistema (1 min)**
```bash
# Iniciar tudo automaticamente
chmod +x scripts/start.sh
./scripts/start.sh
```

#### **3. Acessar Portal (30 seg)**
- **URL:** http://localhost:3000
- **Login:** admin@nimoenergia.com.br
- **Senha:** senha123

---

## 🔧 Comandos Essenciais

### **Verificar Sistema:**
```bash
./scripts/check.sh
```

### **Parar Serviços:**
```bash
# Pressionar Ctrl+C no terminal onde executou ./start.sh
```

### **Reiniciar:**
```bash
./scripts/start.sh
```

---

## 🆘 Problemas Comuns

### **❌ "Permission denied"**
```bash
chmod +x scripts/*.sh
```

### **❌ "Port already in use"**
```bash
# Matar processos nas portas
pkill -f "python.*main.py"
pkill -f "node.*vite"
```

### **❌ "Module not found"**
```bash
# Reexecutar setup
./scripts/setup.sh
```

---

## 📱 URLs de Acesso

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Portal** | http://localhost:3000 | Interface principal |
| **API** | http://localhost:5000 | Backend API |
| **Health** | http://localhost:5000/api/health | Status da API |

---

## 🔑 Credenciais de Teste

| Perfil | Email | Senha |
|--------|-------|-------|
| **Admin** | admin@nimoenergia.com.br | senha123 |
| **Transportadora** | silva@silvatransportes.com.br | senha123 |

---

## 📖 Documentação Completa

- **Instalação Detalhada:** `GUIA_INSTALACAO_LOCAL.md`
- **Problemas e Soluções:** `TROUBLESHOOTING.md`
- **Documentação do Projeto:** `README.md`

---

**🎉 Pronto! Seu Portal NIMOENERGIA está funcionando localmente!**

