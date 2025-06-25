# 🔒 Política de Segurança - Portal NIMOENERGIA

## 📋 Versões Suportadas

Atualmente, oferecemos suporte de segurança para as seguintes versões:

| Versão | Suporte de Segurança |
| ------ | -------------------- |
| 2.0.x  | ✅ Suportada         |
| 1.9.x  | ✅ Suportada         |
| 1.8.x  | ⚠️ Suporte limitado  |
| < 1.8  | ❌ Não suportada     |

## 🚨 Reportando Vulnerabilidades

### Processo de Reporte

Se você descobrir uma vulnerabilidade de segurança, por favor **NÃO** abra uma issue pública. Em vez disso, siga este processo:

1. **Envie um email** para: security@nimoenergia.com.br
2. **Inclua** todas as informações detalhadas
3. **Aguarde** nossa confirmação de recebimento (24-48h)
4. **Colabore** conosco durante a investigação
5. **Aguarde** a divulgação coordenada

### Informações Necessárias

Inclua as seguintes informações em seu reporte:

- **Descrição** detalhada da vulnerabilidade
- **Passos** para reproduzir o problema
- **Impacto** potencial da vulnerabilidade
- **Versões** afetadas
- **Ambiente** onde foi descoberta
- **Evidências** (screenshots, logs, etc.)
- **Sugestões** de correção (se houver)

### Template de Reporte

```
Assunto: [SECURITY] Vulnerabilidade em [Componente]

Descrição:
[Descrição detalhada da vulnerabilidade]

Passos para Reproduzir:
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

Impacto:
[Descrição do impacto potencial]

Versões Afetadas:
[Lista das versões afetadas]

Ambiente:
- OS: [Sistema operacional]
- Browser: [Navegador e versão]
- Versão do Portal: [Versão]

Evidências:
[Screenshots, logs, ou outros evidências]

Sugestões de Correção:
[Se houver sugestões]

Contato:
[Seu nome e email para contato]
```

## ⏱️ Tempo de Resposta

### Cronograma de Resposta

- **Confirmação de recebimento**: 24-48 horas
- **Avaliação inicial**: 3-5 dias úteis
- **Investigação completa**: 7-14 dias úteis
- **Correção e patch**: 14-30 dias úteis
- **Divulgação pública**: Após correção

### Classificação de Severidade

#### 🔴 Crítica (24-48h)
- Execução remota de código
- Bypass de autenticação
- Acesso não autorizado a dados sensíveis
- Injeção SQL com acesso a dados

#### 🟠 Alta (3-7 dias)
- Escalação de privilégios
- Cross-Site Scripting (XSS) persistente
- Exposição de informações sensíveis
- Bypass de autorização

#### 🟡 Média (7-14 dias)
- Cross-Site Scripting (XSS) refletido
- Cross-Site Request Forgery (CSRF)
- Exposição de informações não sensíveis
- Denial of Service (DoS)

#### 🟢 Baixa (14-30 dias)
- Problemas de configuração
- Exposição de informações técnicas
- Vulnerabilidades que requerem acesso físico
- Problemas de usabilidade relacionados à segurança

## 🛡️ Medidas de Segurança Implementadas

### Autenticação e Autorização

- **JWT Tokens** com expiração configurável
- **Refresh Tokens** para renovação segura
- **Rate Limiting** para prevenir ataques de força bruta
- **Bloqueio de conta** após tentativas falhadas
- **Autorização baseada em roles** (RBAC)
- **Validação de permissões** em todos os endpoints

### Proteção de Dados

- **Criptografia de senhas** com bcrypt
- **Hash de arquivos** para integridade
- **Validação de entrada** rigorosa
- **Sanitização de dados** antes do armazenamento
- **Logs de auditoria** para todas as ações críticas
- **Backup criptografado** dos dados

### Segurança de Rede

- **HTTPS obrigatório** em produção
- **Headers de segurança** configurados:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Strict-Transport-Security`
  - `Content-Security-Policy`
- **CORS** configurado adequadamente
- **Rate limiting** por IP e usuário

### Segurança de Aplicação

- **Validação de upload** de arquivos
- **Verificação de tipos MIME**
- **Limitação de tamanho** de arquivos
- **Quarentena de arquivos** suspeitos
- **Escape de output** para prevenir XSS
- **Prepared statements** para prevenir SQL injection

### Infraestrutura

- **Containers isolados** com Docker
- **Variáveis de ambiente** para configurações sensíveis
- **Secrets management** adequado
- **Monitoramento de segurança** contínuo
- **Atualizações automáticas** de dependências
- **Scans de vulnerabilidade** regulares

## 🔍 Monitoramento e Detecção

### Logs de Segurança

Monitoramos os seguintes eventos:

- **Tentativas de login** falhadas
- **Acessos não autorizados**
- **Uploads de arquivos** suspeitos
- **Mudanças de configuração**
- **Ações administrativas**
- **Erros de aplicação** críticos

### Alertas Automáticos

- **Múltiplas tentativas** de login falhadas
- **Acessos de IPs** suspeitos
- **Upload de arquivos** maliciosos
- **Uso anômalo** da API
- **Erros de sistema** críticos

### Ferramentas de Monitoramento

- **SIEM** para correlação de eventos
- **IDS/IPS** para detecção de intrusão
- **Vulnerability scanners** automatizados
- **Dependency checking** contínuo
- **Code analysis** estático

## 🚀 Processo de Correção

### Fluxo de Correção

1. **Recebimento** e confirmação do reporte
2. **Triagem** e classificação de severidade
3. **Investigação** detalhada
4. **Desenvolvimento** da correção
5. **Testes** de segurança
6. **Deploy** em ambiente de staging
7. **Validação** da correção
8. **Deploy** em produção
9. **Divulgação** coordenada

### Comunicação

- **Atualizações regulares** para o reporter
- **Notificação** quando a correção estiver disponível
- **Advisory de segurança** público após correção
- **Agradecimento** público (se desejado)

## 🏆 Programa de Recompensas

### Elegibilidade

- **Vulnerabilidades** genuínas e reproduzíveis
- **Primeiro reporte** da vulnerabilidade
- **Seguimento** do processo de divulgação responsável
- **Não exploração** da vulnerabilidade

### Recompensas

| Severidade | Recompensa |
|------------|------------|
| Crítica    | R$ 1.000 - R$ 5.000 |
| Alta       | R$ 500 - R$ 1.000 |
| Média      | R$ 100 - R$ 500 |
| Baixa      | Reconhecimento público |

### Critérios de Exclusão

- **Vulnerabilidades** já conhecidas
- **Ataques de engenharia social**
- **Ataques de força bruta**
- **Spam ou flooding**
- **Problemas de configuração** do usuário
- **Vulnerabilidades** em dependências de terceiros

## 📚 Recursos de Segurança

### Documentação

- [Guia de Configuração Segura](docs/SECURITY_CONFIG.md)
- [Melhores Práticas de Desenvolvimento](docs/SECURE_CODING.md)
- [Checklist de Segurança](docs/SECURITY_CHECKLIST.md)
- [Plano de Resposta a Incidentes](docs/INCIDENT_RESPONSE.md)

### Ferramentas Recomendadas

- **OWASP ZAP** para testes de penetração
- **Bandit** para análise de código Python
- **ESLint Security** para código JavaScript
- **Snyk** para verificação de dependências
- **Docker Bench** para segurança de containers

### Treinamento

- **OWASP Top 10** awareness
- **Secure coding** practices
- **Incident response** procedures
- **Privacy** and data protection

## 📞 Contatos de Segurança

### Equipe de Segurança

- **Email principal**: security@nimoenergia.com.br
- **Email alternativo**: ciso@nimoenergia.com.br
- **Telefone de emergência**: +55 11 9999-9999
- **PGP Key**: [Link para chave pública]

### Horários de Atendimento

- **Segunda a Sexta**: 9h às 18h (BRT)
- **Emergências**: 24/7 via telefone
- **Resposta por email**: Até 24h

## 🔄 Atualizações desta Política

Esta política de segurança é revisada e atualizada regularmente:

- **Revisão trimestral** da política
- **Atualização** conforme novas ameaças
- **Notificação** de mudanças importantes
- **Versionamento** das políticas

### Histórico de Versões

| Versão | Data | Mudanças |
|--------|------|----------|
| 2.0.0  | 2024-01-01 | Política inicial |

## ⚖️ Aspectos Legais

### Divulgação Responsável

- **Não divulgue** vulnerabilidades publicamente antes da correção
- **Não acesse** dados que não lhe pertencem
- **Não interrompa** ou degrade nossos serviços
- **Respeite** a privacidade dos usuários

### Proteção Legal

Comprometemo-nos a:

- **Não processar** pesquisadores que sigam esta política
- **Trabalhar** com você para entender e resolver problemas
- **Reconhecer** suas contribuições publicamente (se desejado)
- **Manter** a confidencialidade de suas informações

---

**Obrigado por ajudar a manter o Portal NIMOENERGIA seguro! 🔒**

Sua contribuição para a segurança é fundamental para proteger nossos usuários e seus dados.

