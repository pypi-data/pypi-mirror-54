#!/usr/bin/env bash

bumpversion minor --tag --commit
git push
dotenv -f env/flit.env run flit publish
portray as_html --overwrite
portray on_github_pages