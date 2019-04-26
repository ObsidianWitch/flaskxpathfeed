#!/bin/sh

export FLASK_APP='app.main:flaskapp'
export FLASK_ENV='development'
flask run
