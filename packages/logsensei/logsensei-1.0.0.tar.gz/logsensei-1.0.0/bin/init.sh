#!/usr/bin/env bash

# exit when any command fails
set -e

# keep track of the last executed command, echo an error message before exiting
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

git init
git remote add origin git@github.com:AdityaSidharta/logsensei.git
pyenv install 3.7.2
pyenv local 3.7.2
pip install pipenv
pipenv sync --python 3.7.2 --dev
pipenv run flit init
