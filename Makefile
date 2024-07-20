.PHONY: init
init:
	python3 -m venv .venv
	. .venv/bin/activate
	.venv/bin/python -m pip install --upgrade pip setuptools wheel
	.venv/bin/python -m pip install pip-tools

lint:
	-pylint common
	-pylint display
	-pylint notes
	-ruff check .
	-yamllint -s .

reinstall-deps:
	.venv/bin/python -m piptools sync requirements.txt dev-requirements.txt

upgrade-deps:
	.venv/bin/python -m piptools compile --no-emit-index-url --upgrade requirements.in

upgrade-dev-deps:
	.venv/bin/python -m piptools compile --no-emit-index-url --upgrade dev-requirements.in

sync.to-leaf:
	rsync -vha --exclude=.git/ --exclude=.venv/ --exclude=.vscode/ --exclude=__pycache__/ --exclude=.ruff_cache/ . leaf.local:leaf-notes

sync.from-leaf.requirements:
	rsync -vha --exclude=.git/ --exclude=.venv/ --exclude=.vscode/ --exclude=__pycache__/ leaf.local:leaf-notes/requirements.txt requirements.txt

sync.from-leaf.dev-requirements:
	rsync -vha --exclude=.git/ --exclude=.venv/ --exclude=.vscode/ --exclude=__pycache__/ leaf.local:leaf-notes/dev-requirements.txt dev-requirements.txt

build:
	docker build -t leaf-notes:local .
