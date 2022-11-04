.PHONY: init
init:
	python3 -m venv .venv
	. .venv/bin/activate
	.venv/bin/python -m pip install --upgrade pip setuptools wheel
	.venv/bin/python -m pip install pip-tools

lint:
	-flake8 .
	-pylint common
	-pylint display
	-pylint notes
	-yamllint -s .

reinstall-deps:
	.venv/bin/python -m piptools sync requirements.txt dev-requirements.txt

upgrade-deps:
	.venv/bin/python -m piptools compile --no-emit-index-url --upgrade requirements.in

upgrade-dev-deps:
	.venv/bin/python -m piptools compile --no-emit-index-url --upgrade dev-requirements.in

sync.to-leaf:
	rsync -vha --exclude=.git/ --exclude=.venv/ --exclude=.vscode/ --exclude=__pycache__/ . leaf.local:leaf-notes

sync.from-leaf.requirements:
	rsync -vha --exclude=.git/ --exclude=.venv/ --exclude=.vscode/ --exclude=__pycache__/ leaf.local:leaf-notes/requirements.txt requirements.txt

build:
	docker build -t leaf-notes:local .
