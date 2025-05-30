This project is based on the algorithms found in [Practical Astronomy with your Calculator or Spreadsheet](https://www.cambridge.org/de/universitypress/subjects/physics/amateur-and-popular-astronomy/practical-astronomy-your-calculator-or-spreadsheet-4th-edition?format=PB&isbn=9781108436076) by Peter Duffett-Smith and Jonathan Zwart.

This is a library of functions, with unit tests, written in Python 3.12, the standard library, unittest framework, and the math module.

All credit for the accuracy and usefulness of these algorithms goes to the original authors.

# Test

To run all tests run this command:

```bash
python -m unittest
```

# Local Development Setup

## Start/Activate a Virtual Environment

Start:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

## Install dependencies

```bash
pip install --upgrade -r requirements.txt
```

# Installation

```bash
pip install af_practical_astronomy
```

# Running

Currently, you will have to manually import these functions into your project if you wish.

# Future plans

- Finish implementing all of the algorithms from the book.
  - Note: skipped section 31, matrix method for coordinate conversions. Will implement later.
- Add a test runner.

# Updating and Repackaging the Project with `setuptools`

To update and repackage this Python project using `setuptools` on macOS, follow these steps:

## 1. Install or Activate the Virtual Environment

It's recommended to use a virtual environment for isolation. If you don't already have a virtual environment, create and activate one:

### Create and start virtual environment:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

## 2. Install Required Dependencies

Ensure that setuptools and wheel are installed in your environment:

```bash
pip install -r requirements.txt
```

## 3. Update version number

```bash
setup(
    version="0.2.0",  # Update this to the new version number
    ...
)
```

## 4. Build the dist

```bash
python3 setup.py sdist bdist_wheel
```

## 5. Upload with `twine`

```bash
twine upload dist/*
```

And enter in the API token when prompted
