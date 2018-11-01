cov-report = true

lint:
	pipenv run flake8 async_pubsub
	pipenv run black -l 100 --check async_pubsub tests

format:
	pipenv run black -l 100 async_pubsub tests

install-dev:
	pipenv install --skip-lock -d

test:
	pipenv run coverage run -m pytest tests
	@if [ $(cov-report) = true ]; then\
    pipenv run coverage combine;\
    pipenv run coverage report;\
	fi

freeze:
	pipenv lock -d

