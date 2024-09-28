This project is based on the algorithms found in [Practical Astronomy with your Calculator or Spreadsheet](https://www.cambridge.org/de/universitypress/subjects/physics/amateur-and-popular-astronomy/practical-astronomy-your-calculator-or-spreadsheet-4th-edition?format=PB&isbn=9781108436076) by Peter Duffett-Smith and Jonathan Zwart.

This is a library of functions, with unit tests, written in Python 3.12, the standard library, unittest framework, and the math module.

All credit for the accuracy and usefulness of these algorithms goes to the original authors.

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

Clone this repo using git.

# Running

Currently, you will have to manually import these functions into your project if you wish.

You can run the tests in your terminal: `python3 {filename}` eg. `python3 time_functions.test.py`

# Future plans

- Finish implementing all of the algorithms from the book.
- EITHER: add to [afmaths](https://pypi.org/project/afmaths/) library
- OR: publish as an indepdendent module, which is preferable
- Spin off `astronomy_types` into its own project
