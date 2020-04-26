# physics

To run the site locally you should run `snowinmars/3800fe` and `snowinmars/3800be` docker images.

## Frontend

The frontend exists in the `/physics-fe` directory.

### Run locally
```
yarn install
yarn run serve
```

To allow lints and fixes enter
```
yarn run lint
```

### Run in docker

```
docker run -p 0.0.0.0:8080:8080 snowinmars/3800fe
```

Host is `http://localhost:8080`

### Build in docker

```
docker build -t snowinmars/3800fe .
```

## Backend

The backend exists in the `/physics-be` directory.

### Run locally on Windows
```
cd ./physics-be

pip install -r requirements.txt
$env:FLASK_APP = 'server/server.py'  # powershell 
set FLASK_APP=server/server.py       # cmd

flask db init      # creates database using SQLALCHEMY_DATABASE_URI variable
flask db migrate   # in /physics-be/server/config.py 
flask db upgrade

flask run --host 0.0.0.0 --port 5000
```

### Run locally on Linux

- Install requirements from `/physics-be/requirements.txt` using your distributive approach
- Set `FLASK_APP` environment variable equals to path to the `physics-be/server/server.py` file
- Run
```
cd ./physics-be

flask db init
flask db migrate
flask db upgrade

flask run --host 0.0.0.0 --port 5000
```

### Run in docker

Interface `0.0.0.0` is required due to Flask server stuff. If the interface will be mismatched you will not be able to communicate with container (it will looks like 404).

The volume should contain sqlite `server.db` file.

```
docker run -v 3800be:/app/server/vol -p 0.0.0.0:5000:5000 snowinmars/3800be
```

### Build in docker

Host is `http://localhost:5000/api`


```
docker build -t snowinmars/3800be .
```
