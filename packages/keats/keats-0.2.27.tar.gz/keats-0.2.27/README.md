# Keats
[![PyPI version](https://badge.fury.io/py/keats.svg)](https://badge.fury.io/py/keats)

![John Keats](assets/keats.jpg)

Keats is an Python build, installation, and workflow manager.

Features include forced change logs, release scripts, and package version control.

## Why

Every Python developer seems to have their own tricks and scripts for
maintaining changelogs, package versions, and managing releases. Rather
than reinventing the wheel everytime you develop a new pacakge, Keats
provides a standard workflow for doing python package releases. No
customization or Makefiles are required.

## Usage

To install **Keats** to your project, run:

```bash
poetry run add --dev keats
```

Verify your installation by running

```bash
poetry run keats keats
```

To list documentation, run keats with no arguments

```bash
poetry run keats
```

To begin version managment by creating a `__version__.py` in
your main package, run

```bash
poetry run keats version up
```

From within your python project, you can access your version number and
other package information using something like (usually in the `__init__.py`
of your main package).

```python
from .__version__.py import __version__, __title__, __authors__ # and so on
```

To bump to the next version and update your change log (for more on change logs, see below)

```
poetry run keats bump
```

To bump to a specific version:

```
poetry run keats bump <optional version>
```

To bump without updating the change log:

```bash
poetry run keats version bump
```


**Changelogs**

Changelogs are important understanding project status and developer intentions. 
Keats encourages an up-to-date changelog by providing an standard interface
for maintaining and updating change logs using the following files:

* `.keats/changelog.json` - JSON formatted list of changes, with version number, dates, and optional change list.
* `.keats/changelog.md` - markdown formatted changelog

The recommended way to use this is to run `keats bump` which will
bump your package version *and* update your change log:

```
poetry run keats bump <optional version>
```

This will provide an interactive script to update your changelog
with a description and a list of changes. Entries are appended to the
`.keats/changelog.json` and saved. The file is then converted to a markdown
file for readability or documentation purposes.

To just update your change log:

```bash
poetry run keats changelog add
```

If you want to just update the `.keats/changelog.md` from the json file,
run:

```bash
poetry run keats changelog up
```

To clear your change logs:

```bash
poetry rubn keats changelog clear
```

## Global installation

To install **Keats** globally, run:

```bash
pip install keats
```

You can then run all of the commands without the `poetry run`
prefix, given that your current directory is a Python project
with a `pyproject.toml` file.