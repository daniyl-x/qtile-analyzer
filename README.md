# Qtile Analyzer
This is a simple Flask web-app for storing and processing Qtile focus activity
logs.\
It has functionality for viewing different stats like total activity time,
time spent per specific program, etc.


## Table of contents
- [Development](#development)
- [License](#license)


## Development
Setup your environment once after clonning the repository:
```sh
python -m venv .venv 
. .venv/bin/activate 
pip install -r requirements.txt
flask init-db
```
Run the development server:
```sh
. .venv/bin/activate
flask run --reload
```

## License
All the original code and configuration files written by me are licensed
under BSD-2-Clause License, which can be found in the [LICENSE](LICENSE) file.

