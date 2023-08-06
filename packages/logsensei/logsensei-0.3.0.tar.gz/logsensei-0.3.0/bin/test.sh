#!/usr/bin/env bash

# exit when any command fails
set -e

# keep track of the last executed command, echo an error message before exiting
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

pipenv sync --dev
pipenv run pylint logsensei
pipenv run flake8 logsensei
pipenv run py.test --cov-report term --cov=logsensei/ -p no:warnings --cov-fail-under=45
