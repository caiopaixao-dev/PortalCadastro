# 🤝 Contribuindo para o Portal NIMOENERGIA

Obrigado por seu interesse em contribuir com o Portal NIMOENERGIA! Este documento fornece diretrizes e informações sobre como contribuir efetivamente para o projeto.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Padrões de Código](#padrões-de-código)
- [Processo de Pull Request](#processo-de-pull-request)
- [Reportando Bugs](#reportando-bugs)
- [Sugerindo Funcionalidades](#sugerindo-funcionalidades)
- [Documentação](#documentação)

## 📜 Código de Conduta

Este projeto adere ao [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, você deve seguir este código. Por favor, reporte comportamentos inaceitáveis para [contato@nimoenergia.com.br](mailto:contato@nimoenergia.com.br).

## 🚀 Como Contribuir

### Tipos de Contribuição

Valorizamos todos os tipos de contribuição:

- 🐛 **Correção de bugs**
- ✨ **Novas funcionalidades**
- 📚 **Melhorias na documentação**
- 🧪 **Testes**
- 🎨 **Melhorias na UI/UX**
- ⚡ **Otimizações de performance**
- 🔒 **Melhorias de segurança**

### Fluxo de Contribuição

1. **Fork** o repositório
2. **Clone** seu fork localmente
3. **Crie** uma branch para sua contribuição
4. **Faça** suas mudanças
5. **Teste** suas mudanças
6. **Commit** seguindo nossos padrões
7. **Push** para seu fork
8. **Abra** um Pull Request

## 🛠️ Configuração do Ambiente

### Pré-requisitos

- **Node.js** 18+
- **Python** 3.11+
- **Git** 2.30+
- **Docker** (opcional, mas recomendado)

### Configuração Inicial

```bash
# 1. Fork e clone o repositório
git clone https://github.com/SEU_USERNAME/PortalCadastro.git
cd PortalCadastro

# 2. Configure o upstream
git remote add upstream https://github.com/caiopaixao-dev/PortalCadastro.git

# 3. Configure o ambiente backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
cp .env.example .env

# 4. Configure o ambiente frontend
cd ../frontend
npm install
cp .env.example .env.local

# 5. Configure o banco de dados
# MySQL
mysql -u root -p
CREATE DATABASE portal_nimoenergia_dev;

# ou SQLite (desenvolvimento)
# Será criado automaticamente

# 6. Execute as migrações
cd ../backend
python -c "from main import initialize_app; initialize_app()"

# 7. Inicie os serviços
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Usando Docker (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USERNAME/PortalCadastro.git
cd PortalCadastro

# 2. Inicie com Docker Compose
docker-compose up --build

# 3. Acesse a aplicação
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# Adminer: http://localhost:8080
```

## 📝 Padrões de Código

### Python (Backend)

```python
# Seguimos PEP 8 e usamos Black para formatação
# Exemplo de função bem documentada

def upload_documento(transportadora_id: int, arquivo: FileStorage) -> Dict[str, Any]:
    """
    Faz upload de um documento para uma transportadora.
    
    Args:
        transportadora_id: ID da transportadora
        arquivo: Arquivo a ser enviado
        
    Returns:
        Dict contendo informações do documento criado
        
    Raises:
        ValidationError: Se o arquivo for inválido
        DatabaseError: Se houver erro na persistência
    """
    if not arquivo or not arquivo.filename:
        raise ValidationError("Arquivo é obrigatório")
    
    # Validar tipo de arquivo
    if not _is_valid_file_type(arquivo.filename):
        raise ValidationError("Tipo de arquivo não permitido")
    
    # Processar upload
    documento = _process_upload(transportadora_id, arquivo)
    
    return {
        'id': documento.id,
        'nome': documento.nome_arquivo_original,
        'status': documento.status
    }
```

### JavaScript/React (Frontend)

```javascript
// Usamos ESLint + Prettier para formatação
// Exemplo de componente bem estruturado

import React, { useState, useEffect } from 'react';
import { uploadDocumento } from '../services/api';

/**
 * Componente para upload de documentos
 * @param {Object} props - Props do componente
 * @param {number} props.transportadoraId - ID da transportadora
 * @param {Function} props.onUploadSuccess - Callback de sucesso
 */
const DocumentUpload = ({ transportadoraId, onUploadSuccess }) => {
  const [arquivo, setArquivo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!arquivo) {
      setErro('Selecione um arquivo');
      return;
    }

    setLoading(true);
    setErro('');

    try {
      const resultado = await uploadDocumento(transportadoraId, arquivo);
      onUploadSuccess(resultado);
      setArquivo(null);
    } catch (error) {
      setErro(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="arquivo" className="block text-sm font-medium">
          Selecionar Arquivo
        </label>
        <input
          id="arquivo"
          type="file"
          onChange={(e) => setArquivo(e.target.files[0])}
          className="mt-1 block w-full"
          accept=".pdf,.doc,.docx"
        />
      </div>
      
      {erro && (
        <div className="text-red-600 text-sm">{erro}</div>
      )}
      
      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {loading ? 'Enviando...' : 'Enviar Documento'}
      </button>
    </form>
  );
};

export default DocumentUpload;
```

### Padrões de Commit

Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Formato
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé opcional]

# Exemplos
feat(auth): adicionar autenticação JWT
fix(upload): corrigir validação de arquivo
docs(api): atualizar documentação de endpoints
style(frontend): aplicar formatação Prettier
refactor(database): otimizar queries de documentos
test(backend): adicionar testes para upload
chore(deps): atualizar dependências do frontend
```

### Tipos de Commit

- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Mudanças na documentação
- **style**: Formatação, ponto e vírgula, etc
- **refactor**: Refatoração de código
- **test**: Adição ou correção de testes
- **chore**: Tarefas de manutenção

## 🔄 Processo de Pull Request

### Antes de Abrir um PR

1. **Sincronize** com o upstream:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Crie** uma branch descritiva:
   ```bash
   git checkout -b feat/upload-multiplos-arquivos
   ```

3. **Faça** suas mudanças seguindo os padrões

4. **Teste** suas mudanças:
   ```bash
   # Backend
   cd backend
   pytest
   flake8 .
   black --check .
   
   # Frontend
   cd frontend
   npm test
   npm run lint
   npm run build
   ```

5. **Commit** suas mudanças:
   ```bash
   git add .
   git commit -m "feat(upload): permitir upload de múltiplos arquivos"
   ```

### Abrindo o PR

1. **Push** para seu fork:
   ```bash
   git push origin feat/upload-multiplos-arquivos
   ```

2. **Abra** o PR no GitHub

3. **Preencha** o template de PR completamente

4. **Aguarde** a revisão

### Durante a Revisão

- **Responda** aos comentários construtivamente
- **Faça** as mudanças solicitadas
- **Mantenha** a discussão focada no código
- **Seja** paciente e respeitoso

## 🐛 Reportando Bugs

### Antes de Reportar

1. **Verifique** se o bug já foi reportado
2. **Teste** em ambiente limpo
3. **Colete** informações detalhadas

### Informações Necessárias

- **Versão** do sistema
- **Ambiente** (OS, browser, etc.)
- **Passos** para reproduzir
- **Comportamento** esperado vs atual
- **Screenshots** ou logs
- **Dados** de contexto

### Template de Bug Report

Use nosso [template de bug report](.github/ISSUE_TEMPLATE/bug_report.md) para garantir que todas as informações necessárias sejam fornecidas.

## ✨ Sugerindo Funcionalidades

### Processo de Sugestão

1. **Verifique** se a funcionalidade já foi sugerida
2. **Descreva** o problema que resolve
3. **Proponha** uma solução detalhada
4. **Considere** o impacto e complexidade

### Template de Feature Request

Use nosso [template de feature request](.github/ISSUE_TEMPLATE/feature_request.md) para estruturar sua sugestão.

## 📚 Documentação

### Tipos de Documentação

- **README**: Visão geral e quick start
- **API**: Documentação de endpoints
- **Técnica**: Arquitetura e implementação
- **Usuário**: Guias de uso
- **Contribuição**: Este documento

### Padrões de Documentação

- **Markdown** para todos os documentos
- **Linguagem clara** e objetiva
- **Exemplos práticos** sempre que possível
- **Estrutura consistente** entre documentos
- **Atualização** junto com mudanças de código

### Contribuindo com Documentação

```bash
# 1. Identifique a necessidade
# 2. Crie/edite o documento
# 3. Teste os exemplos
# 4. Revise a gramática
# 5. Abra um PR
```

## 🧪 Testes

### Estratégia de Testes

- **Unitários**: Funções e métodos individuais
- **Integração**: Interação entre componentes
- **E2E**: Fluxos completos de usuário
- **Performance**: Carga e stress

### Executando Testes

```bash
# Backend - Todos os testes
cd backend
pytest

# Backend - Com cobertura
pytest --cov=. --cov-report=html

# Frontend - Todos os testes
cd frontend
npm test

# Frontend - Com cobertura
npm run test:coverage

# E2E (se configurado)
npm run test:e2e
```

### Escrevendo Testes

```python
# Exemplo de teste backend
import pytest
from main import app, db
from models.documento import Documento

class TestDocumentoAPI:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                db.drop_all()

    def test_upload_documento_sucesso(self, client):
        # Arrange
        data = {
            'tipo_documento_id': 1,
            'arquivo': (io.BytesIO(b'test content'), 'test.pdf')
        }
        
        # Act
        response = client.post('/api/documentos', data=data)
        
        # Assert
        assert response.status_code == 201
        assert 'id' in response.json
```

```javascript
// Exemplo de teste frontend
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import DocumentUpload from './DocumentUpload';

describe('DocumentUpload', () => {
  test('deve exibir erro quando nenhum arquivo é selecionado', async () => {
    // Arrange
    const onUploadSuccess = jest.fn();
    render(<DocumentUpload transportadoraId={1} onUploadSuccess={onUploadSuccess} />);
    
    // Act
    fireEvent.click(screen.getByText('Enviar Documento'));
    
    // Assert
    await waitFor(() => {
      expect(screen.getByText('Selecione um arquivo')).toBeInTheDocument();
    });
  });
});
```

## 🏷️ Labels e Milestones

### Labels Principais

- **bug**: Correção de problemas
- **enhancement**: Novas funcionalidades
- **documentation**: Melhorias na documentação
- **good first issue**: Bom para iniciantes
- **help wanted**: Ajuda necessária
- **priority/high**: Alta prioridade
- **status/in-progress**: Em desenvolvimento
- **status/needs-review**: Precisa de revisão

### Milestones

- **v1.0.0**: Funcionalidades básicas
- **v1.1.0**: Melhorias de UX
- **v2.0.0**: Funcionalidades avançadas

## 🎯 Roadmap

### Próximas Funcionalidades

- [ ] Upload em lote de documentos
- [ ] Notificações em tempo real
- [ ] Dashboard avançado
- [ ] API mobile
- [ ] Integração com sistemas externos

### Como Contribuir com o Roadmap

1. **Participe** das discussões
2. **Vote** nas funcionalidades
3. **Implemente** funcionalidades prioritárias
4. **Teste** funcionalidades beta

## 📞 Suporte

### Canais de Comunicação

- **Issues**: Para bugs e funcionalidades
- **Discussions**: Para perguntas gerais
- **Email**: contato@nimoenergia.com.br
- **Slack**: [Link do workspace]

### Horários de Suporte

- **Segunda a Sexta**: 9h às 18h (BRT)
- **Resposta**: Até 48h úteis
- **Urgências**: Email com [URGENTE] no assunto

## 🏆 Reconhecimento

### Contribuidores

Todos os contribuidores são reconhecidos em nosso [Hall da Fama](CONTRIBUTORS.md).

### Como Ser Reconhecido

- **Contribuições** regulares
- **Qualidade** do código
- **Ajuda** à comunidade
- **Documentação** e tutoriais

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [Licença MIT](LICENSE).

---

**Obrigado por contribuir com o Portal NIMOENERGIA! 🚀**

Sua contribuição ajuda a tornar o sistema melhor para todos os usuários.

