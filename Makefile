.PHONY: init
init:
	python3 -m venv .venv
	. .venv/bin/activate
	.venv/bin/python -m pip install --upgrade pip setuptools wheel
	.venv/bin/python -m pip install pip-tools

lint:
	-ruff format --check .
	-ruff check .
	-yamllint -s .
	-pylint common
	-pylint display
	-pylint notes

reinstall-deps:
	.venv/bin/python -m piptools sync requirements.txt dev-requirements.txt

upgrade-deps:
	.venv/bin/python -m piptools compile --no-emit-index-url --strip-extras --upgrade requirements.in

upgrade-dev-deps:
	.venv/bin/python -m piptools compile --no-emit-index-url --strip-extras --upgrade dev-requirements.in

sync.to-leaf:
	rsync -vha --exclude=.git/ --exclude=.venv/ --exclude=.vscode/ --exclude=__pycache__/ --exclude=.ruff_cache/ . leaf.local:leaf-notes

sync.from-leaf.requirements:
	rsync -vha leaf.local:leaf-notes/requirements.txt requirements.txt

sync.from-leaf.dev-requirements:
	rsync -vha leaf.local:leaf-notes/dev-requirements.txt dev-requirements.txt

build:
	docker build -t leaf-notes:local .

build.arm64:
	docker build --platform=linux/arm64 --no-cache -t leaf-notes:local-arm64 .
