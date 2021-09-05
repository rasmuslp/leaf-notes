.PHONY: init
init:
	python3 -m venv .venv
	. .venv/bin/activate
	.venv/bin/python -m pip install --upgrade pip setuptools wheel
	.venv/bin/python -m pip install pip-tools

lint:
	-flake8 .
	-pylint display
	-pylint notes
	-yamllint -s .

reinstall-deps:
	.venv/bin/python -m piptools sync requirements.txt dev-requirements.txt

upgrade-deps:
	.venv/bin/python -m piptools compile --upgrade requirements.in
	.venv/bin/python -m piptools compile --upgrade dev-requirements.in
