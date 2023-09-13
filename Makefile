MANAGE := python manage.py

dev:
	@$(MANAGE) runserver

mess:
	python manage.py makemessages -l ru -i venv

compile:
	python manage.py compilemessages

lint:
	poetry run flake8 task_manager

test:
	poetry run pytest -vv -s

test-coverage:
	poetry run coverage run --source="task_manager" manage.py test task_manager
	poetry run coverage xml

check: lint test

install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

.PHONY: dev lint test test-coverage check install build publish package-install