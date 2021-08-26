# leaf-notes

![CI](https://github.com/rasmuslp/leaf-notes/workflows/CI/badge.svg)

## Getting started
Create and activate virtual environment for packages
```
python3 -m venv .venv
source .venv/bin/activate
```

Deactivate virtual environment
```
deactivate
```

## Running the program
Be sure this is python3 at this point
```
python src/main.py
```

## Upgrading packages
1. Be sure to deactivate venv, iff active
    ```
    deactivate
    ```
2. Remove the venv
    ```
    rm -rf .venv
    ```
3. Recreate venv and `activate`
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4. Upgrade pip
    ```
    pip install --upgrade pip
    ```
4. Install packages
    ```
    pip install -e 'git+https://github.com/waveshare/e-Paper.git#egg=waveshare-epd&subdirectory=RaspberryPi_JetsonNano/python'
    pip install pyyaml
    pip install flake8
    pip install pylint
    pip install yamllint
    ```
5. Freeze
    ```
    pip freeze > requirements.txt
    ```

### Projects used
* https://github.com/waveshare/e-Paper - eInk display interface
    * This installs deps for Jetson!
        * https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/setup.py
    * Consider https://github.com/txoof/epdlib ???
* https://github.com/yaml/pyyaml/ - Yaml loader / (de)serializer
    * https://pyyaml.org/wiki/PyYAMLDocumentation
* https://github.com/PyCQA/flake8 - Tooling
* https://github.com/PyCQA/pylint - Tooling
    * List of builtin rules: http://pylint.pycqa.org/en/latest/technical_reference/features.html
    * `pylint --generate-rcfile | less` to generate a rules reference
* https://github.com/adrienverge/yamllint - Tooling

