# View Dependency Resolver

**(also provided Traditional Chinese version document [README-CH.md](README-CH.md).)**

Automatically parse the dependencies of views in the database (Doris) and flatten them into a YAML file.

## Overview

- Language: Python v3.12

## ENV

copy `.env.example` and rename as `.env`

```
DB_HOST=localhost
DB_PORT=9030
DB_USER=root
DB_PASSWORD=
DB_NAME=database
```


## Run

### Install Modules

```
pip install -r requirements.txt
```


### Run

```
python main.py
```