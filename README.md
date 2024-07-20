# leaf-notes

> An application that generates information to be displayed on a small e-ink screen attached to a Raspberry Pi Zero 2 W.

Provided as a Docker image, that through SPI / GPIO controls an e-ink screen.

![CI](https://github.com/rasmuslp/leaf-notes/workflows/CI/badge.svg)

## Hardware
* Raspberry Pi Zero 2 W
* Waveshare e-ink display: 
	https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(B)
    Specs:
		* Colour: Black / Red / White
        * Resolution: 212x104
	Revision: 2.1 V3

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

**`python -m notes`**
Notes module generates notes and saves these as images
```
usage: python -m notes [-h] [-v | -q] --quotes-path path --weather-latitude degrees --weather-longitude degrees --weather-altitude height [-u] [-r degrees]

Generates leaf-note as images

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -q, --quiet           decrease verbosity to absolute minimum
  --quotes-path path    Path to yaml file with Quote definitions
  --weather-latitude degrees
                        Latitude for weather information
  --weather-longitude degrees
                        Longitude for weather information
  --weather-altitude height
                        Height above sea level in meters
  -u, --update-display  Invoke display module to also update the display
  -r degrees, --rotate degrees
                        Rotate image a number of degrees, defaults to 0
```

**`python -m display`**
Display module can clear display and render images to display
```
usage: python -m display [-h] [-v | -q] {clear,render} ...

Handles redering to an e-paper display over SPI on a Raspberry Pi

positional arguments:
  {clear,render}  A command must be specified
    clear         Clear the screen
    render        Render images to screen (clears before rendering)

optional arguments:
  -h, --help      show this help message and exit
  -v, --verbose   increase output verbosity
  -q, --quiet     decrease verbosity to absolute minimum
```

**`python -m display render`**
Render command options
```
usage: python -m display render [-h] -b path -c path [-r degrees]

optional arguments:
  -h, --help            show this help message and exit
  -b path, --black-image path
                        Path to black part of image, required
  -c path, --colour-image path
                        Path to color part of image, required
  -r degrees, --rotate degrees
                        Rotate image a number of degrees, defaults to 0
```

## Running the program as a Docker container
Pull image
```
docker pull ghcr.io/rasmuslp/leaf-notes:<version>
```

Run a one-time container.  
Access to `gpiochip0` and `spidev0.0` is required to communicate with the display. Quotes file needs to be mounted into the container.
```shell
docker run -it --rm \
	--device /dev/gpiochip0 \
	--device /dev/spidev0.0 \
	-v /path-to/quotes.yml:/usr/src/app/quotes.yml:ro \
	-e QUOTES_PATH=quotes.yml \
	-e WEATHER_LATITUDE=50 \
	-e WEATHER_LONGITUDE=10 \
	-e WEATHER_ALTITUDE=10 \
	-e UPDATE_DISPLAY=1 \
	--name leaf-notes \
	ghcr.io/rasmuslp/leaf-notes:<version> python -m notes
```
Options can be set with environment variables
| ENV VAR | Name | Required  
| ------- | ---- | -------- |
|`VERBOSE`| `verbose` | |
|`QUIET`| `quiet` | |
|`QUOTES_PATH`| `quotes-path` | Yes |
|`WEATHER_LATITUDE`| `weather-latitude` | Yes |
|`WEATHER_LONGITUDE`| `weather-longitude` | Yes |
|`WEATHER_ALTITUDE`| `weather-altitude` | |
|`UPDATE_DISPLAY`| `update-display` | |
|`ROTATE`| `rotate` | |

## Upgrading packages
```shell
make upgrade-deps
```

### Projects used
* https://github.com/waveshare/e-Paper - eInk display interface
    * This installs deps for Jetson!
        * https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/setup.py
    * Consider https://github.com/txoof/epdlib ??? - Requires spidev and RPi.GPIO, which cant install on mac.... 
* https://github.com/yaml/pyyaml/ - Yaml loader / (de)serializer
    * https://pyyaml.org/wiki/PyYAMLDocumentation
* https://github.com/dbader/schedule - Scheduler
	* https://pypi.org/project/schedule/
	* https://schedule.readthedocs.io/en/stable/
* https://github.com/PyCQA/pylint - Tooling
    * List of builtin rules: http://pylint.pycqa.org/en/latest/technical_reference/features.html
    * `pylint --generate-rcfile | less` to generate a rules reference
* https://github.com/astral-sh/ruff - Tooling
* https://github.com/adrienverge/yamllint - Tooling

## Docker

Build for development
```shell
docker build -t leaf-notes:local-development -f dev.dockerfile .
```

Build for production
```shell
docker build -t leaf-notes:local .
docker build -t leaf-notes:local-alpine -f alpine.dockerfile .
```

### Notes

**venv in Docker**  
https://medium.com/@elhayefrat/virtualenv-inside-docker-ab26f63ce6d1

**Set unbuffered to ensure all logs from Python are delivered to container std our / err**  
https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED

**Dependencies for Pillow**  
See list of external dependencies here https://pillow.readthedocs.io/en/latest/installation.html#external-libraries  
See Docker Debian Buster example here https://github.com/python-pillow/docker-images/blob/master/debian-10-buster-x86/Dockerfile

