Sticky Notes App
================
A flask/postgres demo app.

Getting Started
===============
To start the application run in shell
```
docker-compose up -d
```
If it is the first launch, also run the following to create DB schema: 
```
docker-compose run flask /usr/local/bin/python db_create.py
```
and then visit [http://localhost:8080/](http://localhost:8080/).

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


