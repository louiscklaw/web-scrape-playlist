#!/usr/bin/env bash

set -ex

cd src

  pipenv run python3 runtest.py

cd ..
