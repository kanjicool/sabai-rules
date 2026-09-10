.PHONY: help venv install test seed verify clean

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
	@echo "  make seed       - Seed Neo4j Knowledge Graph"
	@echo "  make verify     - Run Knowledge Graph verification suite"
	@echo "  make test       - Run pytest unit test suite"
	@echo "  make up         - Start Neo4j via Docker Compose"
	@echo "  make down       - Stop Neo4j containers"

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

test:
	$(VENV_PYTEST) -v
