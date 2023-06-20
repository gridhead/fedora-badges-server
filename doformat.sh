#!/bin/sh

black --line-length=100 badgesdb/
isort --profile=black badgesdb/
flake8 --max-line-length=100 badgesdb/
