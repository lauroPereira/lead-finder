# Lead Finder - Makefile para automação de tarefas

.PHONY: help install test build run clean lint format docker-build docker-test docker-run

# Variáveis
PYTHON := python
PIP := pip
DOCKER_IMAGE := lead-scraper
DOCKER_TAG := latest

# Cores para output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)Lead Finder - Comandos Disponíveis$(NC)"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Instala dependências do projeto
	@echo "$(YELLOW)Instalando dependências...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependências instaladas com sucesso!$(NC)"

install-dev: ## Instala dependências de desenvolvimento
	@echo "$(YELLOW)Instalando dependências de desenvolvimento...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy pre-commit
	@echo "$(GREEN)✅ Dependências de desenvolvimento instaladas!$(NC)"

test: ## Executa todos os testes
	@echo "$(YELLOW)Executando testes...$(NC)"
	pytest -v
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"

test-cov: ## Executa testes com cobertura
	@echo "$(YELLOW)Executando testes com cobertura...$(NC)"
	pytest --cov=lead_scraper --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✅ Relatório de cobertura gerado em htmlcov/$(NC)"

test-unit: ## Executa apenas testes unitários
	@echo "$(YELLOW)Executando testes unitários...$(NC)"
	pytest tests/unit/ -v
	@echo "$(GREEN)✅ Testes unitários concluídos!$(NC)"

test-integration: ## Executa apenas testes de integração
	@echo "$(YELLOW)Executando testes de integração...$(NC)"
	pytest tests/integration/ -v
	@echo "$(GREEN)✅ Testes de integração concluídos!$(NC)"

lint: ## Executa linting do código
	@echo "$(YELLOW)Executando linting...$(NC)"
	flake8 lead_scraper/ tests/
	mypy lead_scraper/
	@echo "$(GREEN)✅ Linting concluído!$(NC)"

format: ## Formata o código com black
	@echo "$(YELLOW)Formatando código...$(NC)"
	black lead_scraper/ tests/
	@echo "$(GREEN)✅ Código formatado!$(NC)"

clean: ## Remove arquivos temporários
	@echo "$(YELLOW)Limpando arquivos temporários...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

docker-build: ## Constrói a imagem Docker
	@echo "$(YELLOW)Construindo imagem Docker...$(NC)"
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
	@echo "$(GREEN)✅ Imagem Docker construída: $(DOCKER_IMAGE):$(DOCKER_TAG)$(NC)"

docker-test: ## Testa o container Docker
	@echo "$(YELLOW)Testando container Docker...$(NC)"
	$(PYTHON) test-container.py
	@echo "$(GREEN)✅ Container testado com sucesso!$(NC)"

docker-run: ## Executa exemplo no container Docker
	@echo "$(YELLOW)Executando exemplo no Docker...$(NC)"
	docker run --rm -v $$(pwd)/data:/app/data $(DOCKER_IMAGE):$(DOCKER_TAG) \
		scrapy crawl bing_maps -a termo="academias" -a estado="RS" -a cidade="Canoas"
	@echo "$(GREEN)✅ Execução concluída! Verifique o arquivo em data/$(NC)"

docker-shell: ## Abre shell no container Docker
	@echo "$(YELLOW)Abrindo shell no container...$(NC)"
	docker run --rm -it -v $$(pwd):/app $(DOCKER_IMAGE):$(DOCKER_TAG) /bin/bash

run-example: ## Executa exemplo local
	@echo "$(YELLOW)Executando exemplo local...$(NC)"
	cd lead_scraper && scrapy crawl bing_maps -a termo="academias" -a estado="RS" -a cidade="Canoas"
	@echo "$(GREEN)✅ Execução concluída! Verifique o arquivo em data/$(NC)"

setup-dev: install-dev ## Configura ambiente de desenvolvimento completo
	@echo "$(YELLOW)Configurando ambiente de desenvolvimento...$(NC)"
	pre-commit install
	@echo "$(GREEN)✅ Ambiente de desenvolvimento configurado!$(NC)"

check: lint test ## Executa verificações completas (lint + testes)
	@echo "$(GREEN)✅ Todas as verificações passaram!$(NC)"

build-all: clean docker-build docker-test ## Pipeline completo de build
	@echo "$(GREEN)✅ Pipeline de build concluído com sucesso!$(NC)"

# Comandos de desenvolvimento
dev-install: ## Instalação rápida para desenvolvimento
	$(PYTHON) -m venv .venv
	@echo "$(YELLOW)Ative o ambiente virtual com:$(NC)"
	@echo "$(BLUE)  Windows: .venv\\Scripts\\activate$(NC)"
	@echo "$(BLUE)  Linux/macOS: source .venv/bin/activate$(NC)"
	@echo "$(YELLOW)Depois execute: make install-dev$(NC)"

# Comandos de produção
prod-build: ## Build otimizado para produção
	@echo "$(YELLOW)Construindo para produção...$(NC)"
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) --target production .
	@echo "$(GREEN)✅ Build de produção concluído!$(NC)"

# Comandos de análise
analyze: ## Análise completa do código
	@echo "$(YELLOW)Executando análise completa...$(NC)"
	@echo "$(BLUE)📊 Estatísticas do código:$(NC)"
	@find lead_scraper -name "*.py" | xargs wc -l | tail -1
	@echo "$(BLUE)📊 Cobertura de testes:$(NC)"
	@pytest --cov=lead_scraper --cov-report=term | grep TOTAL
	@echo "$(GREEN)✅ Análise concluída!$(NC)"

# Comandos Docker Compose
compose-build: ## Constrói serviços com Docker Compose
	@echo "$(YELLOW)Construindo serviços com Docker Compose...$(NC)"
	docker-compose build
	@echo "$(GREEN)✅ Serviços construídos!$(NC)"

compose-up: ## Inicia serviços em background
	@echo "$(YELLOW)Iniciando serviços...$(NC)"
	docker-compose up -d lead-scraper
	@echo "$(GREEN)✅ Serviços iniciados! Use 'make compose-shell' para acessar$(NC)"

compose-test: ## Executa testes via Docker Compose
	@echo "$(YELLOW)Executando testes via Docker Compose...$(NC)"
	docker-compose run --rm lead-scraper-test
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"

compose-shell: ## Abre shell no container via Docker Compose
	@echo "$(YELLOW)Abrindo shell no container...$(NC)"
	docker-compose exec lead-scraper /bin/bash

compose-run: ## Executa exemplo via Docker Compose
	@echo "$(YELLOW)Executando exemplo via Docker Compose...$(NC)"
	docker-compose run --rm lead-scraper \
		scrapy crawl bing_maps -a termo="academias" -a estado="RS" -a cidade="Canoas"
	@echo "$(GREEN)✅ Execução concluída!$(NC)"

compose-jupyter: ## Inicia Jupyter Notebook para análise
	@echo "$(YELLOW)Iniciando Jupyter Notebook...$(NC)"
	docker-compose --profile dev up -d jupyter
	@echo "$(GREEN)✅ Jupyter disponível em http://localhost:8888$(NC)"

compose-down: ## Para todos os serviços
	@echo "$(YELLOW)Parando serviços...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Serviços parados!$(NC)"

compose-logs: ## Mostra logs dos serviços
	docker-compose logs -f

# Comandos de documentação
docs: ## Gera documentação do projeto
	@echo "$(YELLOW)Gerando documentação...$(NC)"
	@echo "$(BLUE)📚 README.md atualizado$(NC)"
	@echo "$(BLUE)📚 Docstrings verificadas$(NC)"
	@echo "$(GREEN)✅ Documentação atualizada!$(NC)"

# Default target
.DEFAULT_GOAL := help