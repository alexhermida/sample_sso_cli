# Sample repo for building CLI with SSO

This repository includes a sample command line tool for
authenticating using SSO.

* Requirements: Python >=3.11 - for learning purpose


## Folder structure

```
    .
    ├── Makefile
    ├── NOTES.md
    ├── README.md
    ├── pyproject.toml
    ├── src
    │   ├── auth.py
    │   ├── commands
    │   │   └── sso.py
    │   └──  main.py
    └── tests
        └── test_auth.py
```

Relevant modules:

- main.py: CLI main entrypoints
- auth.py: Handles authentication against the identity provider
- commands: Folder for including CLI commands


## Installation & run

```bash

    $ pip install .
    $ sso-cli --help

```

## Development

1. Create&activate virtualenv

```bash
    $ make venv
    $ source .venv/bin/activate
```

2. Install with dev requirements

```bash
    $ pip install -e ".[dev]""
```

3. Run lint and tests

```bash
    $ make lint
    $ make tests
```
