# Project Setup

[![Production Workflow](https://github.com/tkim91/IS601-Project4/actions/workflows/prod.yml/badge.svg)](https://github.com/tkim91/IS601-Project4/actions/workflows/prod.yml)

* [Production Deployment](https://tk-project4-prod.herokuapp.com/)


[![Development Workflow](https://github.com/tkim91/IS601-Project4/actions/workflows/dev.yml/badge.svg)](https://github.com/tkim91/IS601-Project4/actions/workflows/dev.yml)

* [Developmental Deployment](https://tk-project4-dev.herokuapp.com/)

## Running Locally

1. To Build with docker compose:
   docker compose up --build
2. To run tests, Lint, and Coverage report use this command: pytest --pylint --cov

.pylintrc is the config for pylint, .coveragerc is the config for coverage and setup.py is a config file for pytest