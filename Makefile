format:
	poetry run isort chat/
	poetry run black chat/

check:
	poetry run isort chat --check
	poetry run flake8 chat
	poetry run black chat --check
