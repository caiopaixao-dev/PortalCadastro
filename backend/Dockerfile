# Multi-stage build para otimização
FROM python:3.11-slim as builder

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro para cache de layers
COPY backend/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage final
FROM python:3.11-slim

# Instalar dependências runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash app

# Copiar dependências do builder
COPY --from=builder /root/.local /home/app/.local

# Criar diretório de trabalho
WORKDIR /app

# Copiar código da aplicação
COPY backend/ .

# Ajustar permissões
RUN chown -R app:app /app

# Mudar para usuário não-root
USER app

# Adicionar .local/bin ao PATH
ENV PATH=/home/app/.local/bin:$PATH

# Variáveis de ambiente
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Porta da aplicação
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')" || exit 1

# Comando para iniciar a aplicação
CMD ["python", "main.py"]

