.PHONY: help install test lint run clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "install    - Install dependencies"
	@echo "test      - Run tests"
	@echo "lint      - Run code quality checks"
	@echo "run       - Run development server"
	@echo "clean     - Clean up project files"
	@echo "docker-build - Build Docker image"
	@echo "docker-run   - Run in Docker container"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install pre-commit
	pre-commit install

test:
	python manage.py test
	coverage run manage.py test
	coverage report

lint:
	black .
	flake8 .
	mypy .
	isort .

run:
	python manage.py migrate
	python manage.py runserver

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +

docker-build:
	docker build -t waselni:latest .

docker-run:
	docker-compose up