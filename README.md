# leaf-notes

> An application that generates information to be displayed on a small e-ink screen attached to a Raspberry Pi Zero W.

Provided as a Docker image, that through SPI / GPIO controls an e-ink screen.

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
    ```shell
    deactivate
    ```
2. Remove the venv
    ```shell
    rm -rf .venv
    ```
3. Recreate venv and `activate`
    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4. Upgrade pip
    ```shell
    pip install --upgrade pip
    ```
4. Install tools
    ```shell
    pip install wheel
    pip install flake8
    pip install pylint
    pip install yamllint
    ```
    Freeze
    ```shell
    pip freeze > requirements-tools.txt
    ```
5. Install packages - Go back to step 1 and start over, this time installing packages instead of tools
    ```shell
    pip install wheel
    pip install pyyaml
    pip install spidev
    pip install RPi.GPIO
    pip install epdlib
    pip install -e 'git+https://github.com/waveshare/e-Paper.git@1ac5cbad562ed58c678ba0d6f3f833612ec53320#egg=waveshare_epd&subdirectory=RaspberryPi_JetsonNano/python'
    pip uninstall -y Jetson.GPIO
    ```
    Freeze
    ```shell
    pip freeze > requirements.txt
    ```

Finally, install needed requirements files.

### Projects used
* https://github.com/waveshare/e-Paper - eInk display interface
    * This installs deps for Jetson!
        * https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/setup.py
    * Consider https://github.com/txoof/epdlib ??? - Rrequires spidev and RPi.GPIO, which cant install on mac.... 
* https://github.com/yaml/pyyaml/ - Yaml loader / (de)serializer
    * https://pyyaml.org/wiki/PyYAMLDocumentation
* https://github.com/PyCQA/flake8 - Tooling
    * https://flake8.pycqa.org/en/latest/index.html
* https://github.com/PyCQA/pylint - Tooling
    * List of builtin rules: http://pylint.pycqa.org/en/latest/technical_reference/features.html
    * `pylint --generate-rcfile | less` to generate a rules reference
* https://github.com/adrienverge/yamllint - Tooling

## Docker

Build for development
```shell
docker build -t leaf-notes:local-development -f Dockerfile.dev .
```

Build for production
```shell
docker build -t leaf-notes:local-latest .
docker build -t leaf-notes:local-alpine -f Dockerfile.alpine .
```

### Notes

**venv in Docker**  
https://medium.com/@elhayefrat/virtualenv-inside-docker-ab26f63ce6d1

**Set unbuffered to ensure all logs from Python are delivered to container std our / err**  
https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED

**Dependencies for Pillow**  
See list of external dependencies here https://pillow.readthedocs.io/en/latest/installation.html#external-libraries  
See Docker Debian Buster example here https://github.com/python-pillow/docker-images/blob/master/debian-10-buster-x86/Dockerfile

