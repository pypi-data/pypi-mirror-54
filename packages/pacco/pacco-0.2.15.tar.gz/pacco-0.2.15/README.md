[![Build Status](https://travis-ci.org/kwinata/pacco.svg?branch=master)](https://travis-ci.org/kwinata/pacco)
[![PyPi version](https://pypip.in/v/pacco/badge.png)](https://pypi.org/project/pacco/)
[![Maintainability](https://api.codeclimate.com/v1/badges/25d9932adf5b9cb51bbe/maintainability)](https://codeclimate.com/github/kwinata/pacco/maintainability)

# Pacco
![](docs/source/_images/pacco.png)

Pacco is a simple package manager (used for prebuilt binary) that is interoperable with Nexus repository manager.

## Usage

To download a registry, run `pacco download <registry> <path> <param=value> (<param=value> ...)`.

## Install
```
pip install pacco
```

## CLI Test

You need to have [bats](https://github.com/sstephenson/bats) installed in order to run tests for CLI.
```
bats tests/cli.bats
```
