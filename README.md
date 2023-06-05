# PAD-US-API

# Installation
1. Clone the repository
```shell
git clone git@github.com:jsolly/PAD-US-API.git
```
2. Install dependencies ()
```shell
$ brew install python3 # I used Python 3.10.9
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

# Configuration
rename sample.env to .env and add your own credentials for SECRET_KEY
The Datbase is committed to source control (sqlite3) for ease of use. This is not recommended for production use.
```shell
$ python3 US_PAD/manage.py migrate
``` 

# Usage
1. Run the server
```shell
$ python3 US_PAD/manage.py runserver
``` 
2. Submit GET requests to
```shell
http://localhost:8000/padapi/aoi-intersect // For a list of intersecting PAD-US areas of interest
http://localhost:8000/padapi/aoi-overlap // For a list of overlapping PAD-US areas of interest
```
See US_PAD/tests.py for example requests

# Testing
1. Run the tests
```shell
$ cd PAD-US-API
$ pytest
```

# Linting
1. Run the linter
```shell
$ cd PAD-US-API
$ ruff --config ./config/pyproject.toml US_PAD  
```

# Formatting
1. Run the formatter
```shell
$ cd PAD-US-API
$ black --config ./config/pyproject.toml US_PAD
```

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
