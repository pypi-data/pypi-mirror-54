[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPI Version](https://img.shields.io/pypi/v/simple-google-vision.svg)](https://pypi.org/project/simple-google-vision/)
[![build status](http://img.shields.io/travis/robmarkcole/simple-google-vision/master.svg?style=flat)](https://travis-ci.com/robmarkcole/simple-google-vision)

# simple-google-vision
Unofficial helper utilities for using the [Google Vision API](https://pypi.org/project/google-cloud-vision/). Currently supports object detection with functions for processing the list of objects returned by the API. See the [`usage.ipynb`](https://github.com/robmarkcole/simple-google-vision/blob/master/usage.ipynb) notebook for usage.

## Google Vision API key file & API Pricing
Follow the instructions on https://cloud.google.com/docs/authentication/getting-started to download your Google Vision API key, which is a `.json` file. 

[Read pricing](https://cloud.google.com/vision/pricing). The first 1000 calls per month are free, additional calls are charged. 

## Development
* Use `venv` -> `python3 -m venv venv` & `source venv/bin/activate`
* `pip install -e .`
* `pip install -r requirements-dev.txt`
* Run tests with `venv/bin/pytest tests/* --disable-warnings`
* Black format with `venv/bin/black gvision/core.py` and `venv/bin/black tests/test_gvision.py`