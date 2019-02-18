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

# Open the app in your browser
$ heroku open
```
