SHELL            = bash
PYTHON           = python3
PIPENV           = pipenv

VENV             = .venv

TARGET           = testpypi


.PHONY: usage
usage:
	@echo "Usage: ${MAKE} TARGET"
	@echo ""
	@echo "Targets:"
	@echo "  init           init for develop"
	@echo "  test           run pytest"
	@echo "  build          package build"
	@echo "  upload         upload to ${TARGET}"
	@echo "    TARGET=pypi  upload to pypi"
	@echo "  lint           run flake8"
	@echo "  format         run some formatter"
	@echo "  clean          clean current directory"

.PHONY: init
init:
	${PIPENV} install -d

.PHONY: test
test:
	${PIPENV} run python -m pytest tests

.PHONY: build
build:
	${MAKE} -s clean
	${PIPENV} run python setup.py sdist bdist_wheel
	${PIPENV} run twine check dist/*

.PHONY: upload
upload:
	${MAKE} -s build
	${PIPENV} run twine upload --repository ${TARGET} dist/*

.PHONY: lint
lint:
	${PIPENV} run flake8 qiitacli tests

.PHONY: format
format:
	${PIPENV} run autoflake -ir \
	    --remove-all-unused-imports \
	    --ignore-init-module-imports \
	    --remove-unused-variables \
	    qiitacli tests
	${PIPENV} run isort -rc qiitacli tests
	${PIPENV} run autopep8 -ir qiitacli tests

.PHONY: clean
clean:
	rm -rf build dist *egg-info
