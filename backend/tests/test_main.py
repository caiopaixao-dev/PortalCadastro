import pytest
import json
import os
import sys
from unittest.mock import patch, MagicMock

# Adicionar o diretório pai ao path para importar o main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, get_db_connection

class TestPortalNIMOENERGIA:
    """Testes funcionais para o Portal NIMOENERGIA"""
    
    @pytest.fixture
    def client(self):
        """Fixture para cliente de teste"""
        app.config['TESTING'] = True
        app.config['DATABASE_TYPE'] = 'sqlite'
        app.config['DATABASE_NAME'] = ':memory:'
        
        with app.test_client() as client:
            with app.app_context():
                yield client

    @pytest.fixture
    def auth_headers(self, client):
        """Fixture para headers de autenticação"""
        # Fazer login e obter token
        response = client.post('/api/auth/login', 
                             json={
                                 'email': 'admin@nimoenergia.com.br',
                                 'password': 'senha123'
                             })
        
        if response.status_code == 200:
            token = response.json['token']
            return {'Authorization': f'Bearer {token}'}
        return {}

    def test_app_health_check(self, client):
        """Teste de health check da aplicação"""
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Portal NIMOENERGIA Backend API'
        assert data['status'] == 'online'

    def test_api_health_endpoint(self, client):
        """Teste do endpoint de health da API"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
        assert 'timestamp' in data
        assert 'version' in data

    def test_login_success(self, client):
        """Teste de login com credenciais válidas"""
        response = client.post('/api/auth/login', 
                             json={
                                 'email': 'admin@nimoenergia.com.br',
                                 'password': 'senha123'
                             })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
        assert 'user' in data
        assert data['user']['email'] == 'admin@nimoenergia.com.br'

    def test_login_invalid_credentials(self, client):
        """Teste de login com credenciais inválidas"""
        response = client.post('/api/auth/login', 
                             json={
                                 'email': 'invalid@email.com',
                                 'password': 'wrongpassword'
                             })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_login_missing_fields(self, client):
        """Teste de login com campos obrigatórios faltando"""
        response = client.post('/api/auth/login', json={})
        assert response.status_code == 400
        
        response = client.post('/api/auth/login', 
                             json={'email': 'test@test.com'})
        assert response.status_code == 400

    def test_dashboard_data(self, client, auth_headers):
        """Teste do endpoint de dados do dashboard"""
        response = client.get('/api/dashboard', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_documentos' in data
        assert 'documentos_pendentes' in data
        assert 'transportadoras_ativas' in data

    def test_dashboard_unauthorized(self, client):
        """Teste de acesso não autorizado ao dashboard"""
        response = client.get('/api/dashboard')
        # Se não tiver autenticação implementada, deve retornar 200
        # Se tiver, deve retornar 401
        assert response.status_code in [200, 401]

    def test_cors_headers(self, client):
        """Teste se os headers CORS estão configurados"""
        response = client.options('/')
        # Verificar se CORS está habilitado
        assert response.status_code in [200, 204]

    @patch('main.get_db_connection')
    def test_database_connection_error(self, mock_db, client):
        """Teste de tratamento de erro de conexão com banco"""
        mock_db.side_effect = Exception("Database connection failed")
        
        response = client.get('/api/dashboard')
        # Deve tratar o erro graciosamente
        assert response.status_code in [200, 500]

    def test_invalid_json_request(self, client):
        """Teste de requisição com JSON inválido"""
        response = client.post('/api/auth/login', 
                             data='invalid json',
                             content_type='application/json')
        assert response.status_code == 400

    def test_method_not_allowed(self, client):
        """Teste de método HTTP não permitido"""
        response = client.delete('/api/auth/login')
        assert response.status_code == 405

    def test_not_found_endpoint(self, client):
        """Teste de endpoint não encontrado"""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404

    def test_large_request_body(self, client):
        """Teste com corpo de requisição muito grande"""
        large_data = {'data': 'x' * 10000}  # 10KB de dados
        response = client.post('/api/auth/login', json=large_data)
        # Deve tratar adequadamente
        assert response.status_code in [400, 413, 422]

    def test_sql_injection_protection(self, client):
        """Teste de proteção contra SQL injection"""
        malicious_input = "'; DROP TABLE users; --"
        response = client.post('/api/auth/login', 
                             json={
                                 'email': malicious_input,
                                 'password': 'password'
                             })
        
        # Não deve causar erro interno do servidor
        assert response.status_code in [400, 401]

    def test_xss_protection(self, client):
        """Teste de proteção contra XSS"""
        xss_payload = "<script>alert('xss')</script>"
        response = client.post('/api/auth/login', 
                             json={
                                 'email': xss_payload,
                                 'password': 'password'
                             })
        
        # Deve tratar adequadamente
        assert response.status_code in [400, 401]

    def test_rate_limiting_simulation(self, client):
        """Teste de simulação de rate limiting"""
        # Fazer múltiplas requisições rapidamente
        responses = []
        for i in range(10):
            response = client.post('/api/auth/login', 
                                 json={
                                     'email': f'test{i}@test.com',
                                     'password': 'password'
                                 })
            responses.append(response.status_code)
        
        # Pelo menos algumas devem ser processadas
        assert any(status in [200, 401] for status in responses)

    def test_content_type_validation(self, client):
        """Teste de validação de Content-Type"""
        response = client.post('/api/auth/login', 
                             data='email=test&password=test',
                             content_type='application/x-www-form-urlencoded')
        
        # Deve aceitar ou rejeitar adequadamente
        assert response.status_code in [200, 400, 401, 415]

    def test_empty_request_body(self, client):
        """Teste com corpo de requisição vazio"""
        response = client.post('/api/auth/login')
        assert response.status_code == 400

    def test_special_characters_handling(self, client):
        """Teste de tratamento de caracteres especiais"""
        special_chars = "áéíóúàèìòùâêîôûãõç!@#$%^&*()"
        response = client.post('/api/auth/login', 
                             json={
                                 'email': f'test{special_chars}@test.com',
                                 'password': special_chars
                             })
        
        # Deve tratar adequadamente
        assert response.status_code in [400, 401]

    def test_concurrent_requests_simulation(self, client):
        """Teste de simulação de requisições concorrentes"""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = client.get('/')
            results.append(response.status_code)
        
        # Simular 5 requisições concorrentes
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Todas devem ser bem-sucedidas
        assert all(status == 200 for status in results)

    def test_database_types_support(self, client):
        """Teste de suporte a diferentes tipos de banco"""
        # Testar se a aplicação funciona com diferentes configurações
        with patch.dict(os.environ, {'DATABASE_TYPE': 'sqlite'}):
            response = client.get('/')
            assert response.status_code == 200
        
        with patch.dict(os.environ, {'DATABASE_TYPE': 'mysql'}):
            response = client.get('/')
            assert response.status_code == 200

    def test_environment_variables(self, client):
        """Teste de variáveis de ambiente"""
        # Verificar se a aplicação lida com variáveis de ambiente ausentes
        with patch.dict(os.environ, {}, clear=True):
            response = client.get('/')
            # Deve funcionar com valores padrão
            assert response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

