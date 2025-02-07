#!/bin/bash
set -e
mypy splashscreen.py --strict --ignore-missing-import
python3 splashscreen.py