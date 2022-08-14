

# Book Store

This is TEST project (on the develop stage). More information will come later

## Setup
####  VSCode + FastAPI + PostgreSQL


## Installation

#### 1. Clone project
#### 2. Create virtual enviroment and enable it
> for example
> ```sh
> python -m venv venv
> source ./venv/bin/activate
> ```

#### 3. Check if poetry is installed in comand line
```sh
poetry --version
```
> if it's **NOT** install [poetry](https://python-poetry.org/docs/#installation)


#### 4.  The `install` command reads the `pyproject.toml` file from the current project, resolves the dependencies, and installs them.
```sh
poetry install
```
> You can specify to the command that you do not want the development dependencies installed by passing the `--no-dev` option.
> ```sh
> poetry install --no-dev
> ```

#### 5. Create your own `PostgreSQL` database
> for example by using pgAdmin4

#### 6. When loading configurations from `.env` file. `Python-Dotenv` package is required.
```sh
poetry add python-dotenv
```

#### 7. Create file `.env` in root directory:
> root_directory/.env >
```sh
# PostgreSQL
POSTGRES_SERVER=localhost
POSTGRES_USER=*youruser*
POSTGRES_PASSWORD=*password*
POSTGRES_DB=*name_of_database*
# For JWT tokens
ACCESS_TOKEN_EXPIRES_MINUTES=*minutes* #minutes
REFRESH_TOKEN_EXPIRES_MINUTES=*minutes* # minutes
SECRET_JWT_KEY=*long string* # (use this command to generate key *openssl rand -hex 32*)
JWT_ALGORITHM=*type*
```

#### 8. Launch our server:
```sh
uvicorn app.main:app --reload
```

