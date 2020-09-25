#!/usr/bin/env bash

set -ex

cd src
  pipenv sync
  nodemon -w . -e * --exec "pipenv run python3 fetch.py"
