# 3800 las project

This is a project that provides access to physics tasks. It maintenance by school students for free. Monetization will never be allowed.

The project could be viewed [here](http://ec2-35-157-38-27.eu-central-1.compute.amazonaws.com/). If you'd like to share the link, please use this page link due to the server host will be changed.

The project provide access to its api. See postman collections files in the git root or contact dev team for information.

## Development

To run the site locally you should run `snowinmars/3800fe` and `snowinmars/3800be` docker images or run these two servers manually outside of docker.

#### Run in docker

###### Frontend

1. Run
```
# ensure that /physics-fe/src/config/api.js > 'apiPrefix' equals to "http://127.0.0.1:5000/api"

cd /physics-fe
docker build -t snowinmars/3800fe .
docker run -p 8080:8080 snowinmars/3800fe
```

On this step you should be able to see the frontend page on `http://localhost:80` with the 'api is dead' warning.

###### Backend

To run backend you should create a database. It could not be automatically created in docker build process due to the database should be available with or without alive docker container.

1. Create a docker volume
    ```
    docker volume create
        --opt type=none
        --opt device=/home/user/docker/3800/
        --opt o=bind
            3800be
    ```
   
1. Create a database in docker volume's folder. In the example above the folder is `/home/user/docker/3800/`.
    
    - You can use test database from `/physics-be/server/tests/test.db`
    - You can ask a developer to provide you a database file.
    - You can create your own database using the guide below.

1. Run
```
# if '/app/server/vol' path below ends with 'vol'
# the '/physics-be/server/config.py > SQLALCHEMY_DATABASE_URI' should contains 'vol' too.

cd /physics-be
docker build -t snowinmars/3800be .
docker run -v 3800be:/app/server/vol -p 0.0.0.0:5000:5000 snowinmars/3800be
```

## Nginx

Nginx is responsable for proxing requests and valicating ssl certificates.

Run
```
cd /nginx
docker buils -t snowinmars/3800ngx .
docker run -p 80:80 snowinmars/3800ngx
```

## How to start developing

#### Frontend

Install `yarn`.

Run

```
cd physics-fe

yarn install
yarn run lint
yarn run serve
```

- To change api host use `/physics-fe/src/config/api.js > apiPrefix` variable.
- `App.vue` styles are not scoped, so it applies globally.
- Do not set color explicitly. Use variables like `--background-primary-color`. See `App.vue` for examples.
- Try to encapsulate data inside components, use global store or local storage only if you have to.
- If your component needs to access the current user, check out how it works in `User.vue`.

#### Backend

1. Install `pip`.

1. Run `pip install --user -r /physics-be/requirements.txt`. It's safe to run on linux due to the `--user` key installs packages to `~` without roaming around with package manager stuff. Of course, if you can, you can try to install python packages with your package manager, but I see that most systems doesn't support all the python packages well.

1. Make an env variable `FLASK_APP` point to `/physics-be/server/server.py`.

    You should run all flask commands from the directory where the `FLASK_APP` will be correct.
    
    The examples below assumes that you're in `/physics-be` folder:
    
    - shell: `export FLASK_APP=server/server.py`
    - cmd: `set FLASK_APP=server/server.py`
    - powershell: `$env:FLASK_APP = 'server/server.py'`

1. Run
    ```
    flask db init
    flask db migrate
    flask db upgrade
    ```

    It uses `/physics-be/server/config.py > SQLALCHEMY_DATABASE_URI` variable so make sure it fit your local path.
   
1. Run `flask run --host 0.0.0.0 --port 5000`

    Interface `0.0.0.0` is required due to Flask server stuff. If the interface will be mismatched you will not be able to communicate with docker container (it will looks like 404). For local runs I prefer to use `0.0.0.0` anyway.

## SSL host setup

* ssh to host
* enter inside nginx containter
* instal `certbot`
* run
```
mkdir -p /var/www/html
certbot -i nginx -a webroot certonly -w /var/www/html -d las3832.ru
```

## FAQ

- How to export sqlite to .sql?
    - `sqlite my.db .dump > data.sql`
