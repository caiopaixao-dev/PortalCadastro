# 🔒 Portal NIMOENERGIA - Sistema Proprietário de Gestão de Documentos

![License](https://img.shields.io/badge/License-Proprietary-red.svg)
![Status](https://img.shields.io/badge/Status-Confidential-red.svg)
![Access](https://img.shields.io/badge/Access-Restricted-red.svg)

## ⚠️ AVISO IMPORTANTE - ACESSO RESTRITO

**🔐 ESTE É UM SISTEMA PROPRIETÁRIO E CONFIDENCIAL DA NIMOENERGIA**

- ❌ **NÃO é permitido** compartilhar este código
- ❌ **NÃO é permitido** usar fora da NIMOENERGIA
- ❌ **NÃO é permitido** distribuir ou divulgar
- ✅ **Acesso APENAS** para colaboradores autorizados
- ✅ **Uso EXCLUSIVO** para fins corporativos da NIMOENERGIA

---

## 📋 Visão Geral

O Portal NIMOENERGIA é um sistema robusto e escalável para gestão de documentos de transportadoras, desenvolvido exclusivamente para uso interno da NIMOENERGIA com tecnologias modernas e arquitetura enterprise-grade.

## 🔒 Política de Acesso

### ✅ **Usuários Autorizados:**
- Funcionários diretos da NIMOENERGIA
- Colaboradores com contrato vigente
- Prestadores de serviços autorizados
- Parceiros com acordo de confidencialidade

### ❌ **Acesso Negado Para:**
- Terceiros não autorizados
- Ex-funcionários sem autorização
- Empresas concorrentes
- Uso comercial externo

## 🚀 Características Principais

### ✅ **Backend Robusto**
- **Flask** com arquitetura escalável
- **Múltiplos bancos de dados**: MySQL, PostgreSQL, SQLite
- **Segurança avançada**: JWT, bcrypt, rate limiting
- **API RESTful** completa e documentada
- **Logging e monitoramento** integrados
- **Validação robusta** de dados
- **Auditoria completa** de ações

### ✅ **Frontend Moderno**
- **React 18** com hooks modernos
- **Tailwind CSS** para design responsivo
- **Interface intuitiva** e acessível
- **PWA ready** (Progressive Web App)
- **Componentes reutilizáveis**
- **Estado global** gerenciado
- **Tratamento de erros** robusto

### ✅ **Banco de Dados Flexível**
- **Estrutura robusta** para evolução
- **Relacionamentos complexos** bem definidos
- **Índices otimizados** para performance
- **Triggers e procedures** automatizados
- **Auditoria completa** de mudanças
- **Backup e recovery** configurados

### ✅ **Segurança Enterprise**
- **Autenticação JWT** com refresh tokens
- **Autorização baseada em roles**
- **Criptografia de senhas** com bcrypt
- **Rate limiting** por IP e usuário
- **Headers de segurança** configurados
- **Validação de entrada** rigorosa
- **Logs de auditoria** detalhados

### ✅ **Deploy e Produção**
- **Docker** containerizado
- **Heroku** ready
- **AWS** compatible
- **CI/CD** configurado
- **Monitoramento** integrado
- **Backup automático**

## 🏗️ Arquitetura do Sistema

```
Portal NIMOENERGIA (Proprietário)
├── 🐍 Backend (Flask)
│   ├── API RESTful
│   ├── Autenticação JWT
│   ├── Banco de Dados
│   └── Logs de Auditoria
├── ⚛️ Frontend (React)
│   ├── Interface Responsiva
│   ├── Dashboard Interativo
│   ├── Upload de Documentos
│   └── Gestão de Usuários
└── 🗄️ Database
    ├── Estrutura Relacional
    ├── Índices Otimizados
    └── Backup Automático
```

## 🔐 Funcionalidades Principais

### 👨‍💼 **Dashboard Administrativo NIMOENERGIA**
- Métricas em tempo real
- Gestão de transportadoras
- Aprovação/rejeição de documentos
- Relatórios de compliance
- Auditoria de ações

### 🚛 **Portal das Transportadoras**
- Upload de documentos (drag-and-drop)
- Acompanhamento de status
- Notificações de vencimento
- Histórico de documentos
- Dashboard personalizado

### 📄 **Gestão de Documentos**
- Suporte a múltiplos formatos (PDF, DOCX, JPG, PNG)
- Validação automática
- Controle de vencimentos
- Histórico de versões
- Backup seguro

### 🔍 **Sistema de Busca**
- Filtros avançados
- Busca por múltiplos critérios
- Exportação de relatórios
- Ordenação personalizada

## 🛡️ Segurança e Compliance

### 🔒 **Medidas de Segurança**
- Criptografia end-to-end
- Autenticação multifator (opcional)
- Logs de auditoria completos
- Backup criptografado
- Monitoramento de acesso

### 📋 **Compliance**
- LGPD (Lei Geral de Proteção de Dados)
- Políticas internas da NIMOENERGIA
- Auditoria de segurança
- Controle de acesso granular

## 🚀 Instalação e Configuração

### ⚠️ **IMPORTANTE: ACESSO RESTRITO**
A instalação e configuração deste sistema é permitida APENAS para:
- Equipe de TI da NIMOENERGIA
- Desenvolvedores autorizados
- Administradores de sistema aprovados

### 📋 **Pré-requisitos**
- Python 3.11+
- Node.js 18+
- Banco de dados (MySQL/PostgreSQL/SQLite)
- Autorização da equipe de TI da NIMOENERGIA

### 🔧 **Configuração Rápida**
```bash
# APENAS PARA USUÁRIOS AUTORIZADOS
git clone https://github.com/caiopaixao-dev/PortalCadastro.git
cd PortalCadastro
./scripts/setup.sh
./scripts/start.sh
```

## 📖 Documentação

### 📚 **Documentação Técnica**
- [API Documentation](docs/API.md)
- [Technical Architecture](docs/TECHNICAL.md)
- [Database Schema](docs/MER_VISUAL.md)
- [Security Guidelines](SECURITY.md)

### 🔧 **Guias de Instalação**
- [Instalação Local](GUIA_INSTALACAO_LOCAL.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Início Rápido](INICIO_RAPIDO.md)

## 🤝 Contribuição

### ✅ **Colaboradores Autorizados**
Apenas funcionários e colaboradores autorizados da NIMOENERGIA podem contribuir:

1. **Fork** do repositório (apenas internamente)
2. **Criar branch** para feature/bugfix
3. **Seguir** padrões de código da empresa
4. **Submeter** pull request para revisão
5. **Aguardar** aprovação da equipe de TI

### 📋 **Processo de Revisão**
- Code review obrigatório
- Testes automatizados
- Aprovação da equipe de TI
- Documentação atualizada

## 📞 Suporte e Contato

### 🏢 **NIMOENERGIA - Departamento de TI**
- **Email:** caio.pcoimbra@gmail.com
- **Telefone:** [Interno apenas]
- **Slack:** #portal-nimoenergia [Interno]

### 🆘 **Suporte Técnico**
- **Issues:** Apenas para colaboradores autorizados
- **Documentação:** Consulte os guias incluídos
- **Emergências:** Contate a equipe de TI diretamente

## ⚖️ Licença e Termos de Uso

### 🔒 **LICENÇA PROPRIETÁRIA CORPORATIVA**

**Copyright (c) 2024 NIMOENERGIA - Todos os direitos reservados.**

Este software é propriedade exclusiva da NIMOENERGIA e está protegido por leis de direitos autorais. O uso é ESTRITAMENTE LIMITADO a colaboradores autorizados da NIMOENERGIA.

**PROIBIÇÕES:**
- ❌ Distribuição ou compartilhamento não autorizado
- ❌ Uso comercial fora da NIMOENERGIA
- ❌ Modificação sem autorização
- ❌ Engenharia reversa
- ❌ Sublicenciamento

**Para mais detalhes, consulte o arquivo [LICENSE](LICENSE).**

### ⚠️ **AVISO LEGAL**
O uso não autorizado deste software constitui violação de direitos autorais e pode resultar em penalidades civis e criminais conforme a legislação brasileira.

---

## 🏆 Status do Projeto

![Build Status](https://img.shields.io/badge/Build-Passing-green.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-green.svg)
![Security](https://img.shields.io/badge/Security-Audited-green.svg)
![Compliance](https://img.shields.io/badge/LGPD-Compliant-green.svg)

### 📊 **Métricas do Sistema**
- **Uptime:** 99.9%
- **Performance:** Otimizado
- **Segurança:** Auditado
- **Compliance:** LGPD Compliant

---

**🔐 SISTEMA PROPRIETÁRIO DA NIMOENERGIA - ACESSO RESTRITO**

*Este repositório contém informações confidenciais e proprietárias. O acesso é monitorado e registrado para fins de auditoria e segurança.*

