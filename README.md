# Flask-XPathFeed

Flask-XPathFeed is a [Flask](http://flask.pocoo.org/) web application to
generate Atom feeds from XPath expressions.

## Deploy

```shell
# Clone this repository
$ git clone https://gitlab.com/Obsidienne/flask-xpathfeed.git

# Create a branch
$ git checkout -b self

# Edit `app/config.py` with your own bridges
$ nano app/config.py

# Commit your changes
$ git commit -am "config - Bandcamp bridge"

# Deploy to Heroku
$ heroku login
$ heroku create
$ git push heroku self:master
```

## Examples

```shell
# Get feed for "AO3 - Warcraft F/F (+ other filters)"
https://example.com/feed?src=https://frama.link/fe3NWkxB

# Get feed for "AO3 - Nyaaru's bookmarks"
https://example.com/feed?src=https://frama.link/Gc4Czmj1

# Get feed for "AO3 - A Better Past by LysSerris"
https://example.com/feed?src=https://frama.link/tfh9yFNz

# Set a custom keyword bookmark in Firefox (e.g. !bridge)
https://example.com/feed?src=%s
```
