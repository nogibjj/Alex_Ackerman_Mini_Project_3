install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --nbval-lax -cov=mylib -cov=main *.py test_*.py *.ipynb

format:	
	black *.py 

lint:
	#disable comment to test speed
	#pylint --disable=R,C --ignore-patterns=test_.*?py *.py mylib/*.py
	#ruff linting is 10-100X faster than pylint
	ruff check *.py mylib/*.py

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

refactor: format lint

deploy:
	#deploy goes here

all: install lint test format deploy

# generate_and_push:
# 	python main.py
# 	git config --local user.email "action@github.com"; \
# 	git config --local user.name "GitHub Action"; \
# 	git add .; \
# 	git commit -m "Add generated plot and report"; \
# 	git push
	

