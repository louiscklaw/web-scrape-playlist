#!/usr/bin/env bash

set -ex

cd src
  pipenv sync
  nodemon -w . -e "py,txt,html" --exec "pipenv run python3 fetch.py"
