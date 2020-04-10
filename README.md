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

### Run locally on Windows

To run it locally enter
```
pip install -r /physics-be/requirements.txt
flask run --host 0.0.0.0 --port 5000
```

### Run locally on Linux

Install requirements from `/physics-be/requirements.txt` using your distributive approach then run
```
flask run --host 0.0.0.0 --port 5000
```

### Build docker image

```
docker build -t las/3800-be .
```

### Run docker image
```
docker run -p 0.0.0.0:5000:5000 las/3800-be
```
