#!/usr/bin/env bash

# exit when any command fails
set -e

# keep track of the last executed command, echo an error message before exiting
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

bumpversion minor --tag --commit
git push
dotenv -f env/flit.env run flit publish
portray as_html --overwrite
portray on_github_pages