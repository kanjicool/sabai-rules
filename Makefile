.PHONY: help venv install test seed verify analytics ingest chatbot rag up down clean

PYTHON ?= python
VENV_DIR ?= .venv

ifeq ($(OS),Windows_NT)
    VENV_PYTHON = $(VENV_DIR)/Scripts/python.exe
    VENV_PIP = $(VENV_DIR)/Scripts/pip.exe
    VENV_PYTEST = $(VENV_DIR)/Scripts/pytest.exe
else
    VENV_PYTHON = $(VENV_DIR)/bin/python
    VENV_PIP = $(VENV_DIR)/bin/pip
    VENV_PYTEST = $(VENV_DIR)/bin/pytest
endif

help:
	@echo "Sabai-Rules Project Management Commands:"
	@echo "  make venv       - Create Python virtual environment"
	@echo "  make install    - Install required dependencies"
	@echo "  make up         - Start Neo4j via Docker Compose"
	@echo "  make down       - Stop Neo4j containers"
	@echo "  make seed       - Seed Neo4j Knowledge Graph"
	@echo "  make verify     - Run Knowledge Graph verification suite"
	@echo "  make analytics  - Run Knowledge Graph Relationship Analysis Report"
	@echo "  make ingest     - Build Vector Store Index from PDF"
	@echo "  make chatbot    - Run FastAPI LINE Chatbot server"
	@echo "  make rag        - Test Vector RAG query via CLI"
	@echo "  make test       - Run pytest unit test suite"

venv:
	$(PYTHON) -m venv $(VENV_DIR)

install:
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements.txt

up:
	docker compose up -d

down:
	docker compose down

seed:
	$(VENV_PYTHON) -m src.graph.seeder

verify:
	$(VENV_PYTHON) -m src.graph.verify_graph

analytics:
	$(VENV_PYTHON) -m src.graph.analytics

ingest:
	$(VENV_PYTHON) -m src.vector.store

chatbot:
	$(VENV_PYTHON) -m src.webhook.server

rag:
	$(VENV_PYTHON) -m src.rag.vector_rag

extract:
	$(VENV_PYTHON) -m src.graph.llm_extractor

eval:
	$(VENV_PYTHON) -m scripts.evaluate_rag_metrics

test:
	$(VENV_PYTEST) -v

