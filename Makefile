MANAGE := python manage.py

dev:
	@$(MANAGE) runserver

mess:
	@$(MANAGE) makemessages -l ru -i venv

compile:
	@$(MANAGE) compilemessages

lint:
	poetry run flake8 task_manager

test:
	@$(MANAGE) test tests

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