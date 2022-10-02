# LNbits Registry

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A backend for managing and serving LNbits extensions.

## Beta Disclaimer
This software is still considered BETA and may contain bugs. Don't expose it to the open internet or use with a lot of funds.

## ToC
- [LNbits Registry](#lnbits-registry)
  - [Beta Disclaimer](#beta-disclaimer)
  - [ToC](#toc)
    - [Dependencies](#dependencies)
  - [Development](#development)
    - [Installation](#installation)
    - [Swagger / OpenAPI](#swagger--openapi)

### Dependencies

- [Python in version 3.10](https://www.python.org/downloads/)
- [Poetry in version 1.2](https://python-poetry.org)

## Development

Clone the repository `git clone git@github.com:fusion44/lnbits-registry.git`

Make sure you have [Poetry](https://python-poetry.org) installed.

From within the `lnbits-registry` folder [open a poetry shell](https://python-poetry.org/docs/master/cli/#shell) via:

```sh
poetry shell
```

(To exit the poetry shell use: `exit`)

### Installation

```
poetry install
```

If python dependencies have been changed it's necessary to freeze all requirements to requirements.txt:

```sh
poetry export -f requirements.txt --output requirements.txt
```

> ℹ️ This will skip all dev dependencies by default.\
> This step is required to avoid having to install poetry for final deployment.

### [Swagger / OpenAPI](https://swagger.io)

Once the API is running swagger docs can be found here:

```
http://127.0.0.1:8000/latest/docs
```
