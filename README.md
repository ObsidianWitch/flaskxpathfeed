# Flask-XPathFeed

Flask-XPathFeed is a [Flask](http://flask.pocoo.org/) web application to
generate Atom feeds from XPath expressions.

## Development

```shell
# Clone this repository
$ git clone https://github.com/obsiwitch/flaskxpathfeed.git
$ cd flask-xpathfeed

# Set up virtual environment
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ ./debug.sh
$ deactivate
```

## Deploy to Heroku

```shell
# Clone this repository
$ git clone https://github.com/obsiwitch/flaskxpathfeed.git
$ cd flask-xpathfeed

# Create a branch
$ git checkout -b self

# Add your own bridges
$ nano app/bridges.py

# Commit your changes
$ git commit -am "Bandcamp bridge"

# Deploy to Heroku
$ heroku login
$ heroku create
$ git push heroku self:master
$ heroku logout
```

## Examples

```shell
# Preview feed
https://example.com/preview?src=https://frama.link/fe3NWkxB

# Get feed for "AO3 - Warcraft F/F (+ other filters)"
https://example.com/feed?src=https://frama.link/fe3NWkxB

# Get feed for "AO3 - Nyaaru's bookmarks"
https://example.com/feed?src=https://frama.link/Gc4Czmj1

# Get feed for "AO3 - A Better Past by LysSerris"
https://example.com/feed?src=https://frama.link/tfh9yFNz

# Set a custom keyword bookmark in Firefox (e.g. !bridge)
https://example.com/feed?src=%s
```
