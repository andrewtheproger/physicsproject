# physics

## Frontend

The frontend exists in the `/physics-fe` directory.

To run it locally enter
```
yarn install
yarn run serve
```

To compile and minify for production enter
```
yarn run build
```

To allow lints and fixes enter
```
yarn run lint
```

## Backend

The backend exists in the `/physics-be` directory.

### tl;dr

```
docker run -p 0.0.0.0:5000:5000 las/3800-be
curl http://127.0.0.1:5000/api/health
```

### Build docker image

```
docker build -t las/3800-be .
```

### Run docker image

Interface `0.0.0.0` is required due to Flask server stuff. If the interface will be mismatched you will not be able to communicate with container (it will looks like 404).

```
docker run -p 0.0.0.0:5000:5000 las/3800-be
```

### Run locally on Windows

To run it locally enter
```
cd ./physics-be

pip install -r /physics-be/requirements.txt
$env:FLASK_APP = 'server/server.py'

flask db init
flask db migrate
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
