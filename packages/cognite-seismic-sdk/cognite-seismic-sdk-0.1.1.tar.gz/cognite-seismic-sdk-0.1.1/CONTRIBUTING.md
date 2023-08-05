## Development Instructions

### Setup

```bash
$ git clone https://github.com/cognitedata/cognite-seismic-sdk.git
$ cd cognite-seismic-sdk
$ pipenv install -d
$ pipenv shell
```

### Testing
Set up tests for all new functionality. Running the tests will require setting the environment variable 'COGNITE_TEST_API_KEY'.

Initiate unit tests by running the following command from the root directory:

`$ pytest`

If you want to generate code coverage reports run:

```
$ pytest --cov-report html \
    --cov-report xml \
    --cov cognite
```

Open `htmlcov/index.html` in the browser to navigate through the report.

### Documentation
Build html files of documentation locally by running

```bash
$ cd docs
$ make html
```
Documentation will be automatically generated from the google-style docstrings in the source code. It is then built and released when changes are merged into master.

### Release version conventions
Release format:

```
MAJOR.MINOR[.MICRO]
```

We use semantic versioning.