import requests
from datetime import datetime
from urllib.parse import urljoin

import lxml.html
import lxml.etree
import flask
from werkzeug.contrib.atom import AtomFeed

from app.types import Table
import app.bridges

class XPathFeed:
    def __init__(self, src):
        request = requests.get(
            url     = src,
            headers = { "user-agent": "Mozilla/5.0" },
        )
        self.source_url = src
        self.resolved_url = request.url

        html = request.content
        tree = lxml.html.fromstring(html)
        self.urlabs(tree, self.resolved_url)

        bridge = next(
            bridge for _, bridge in app.bridges.table.items()
            if bridge.match(self.resolved_url)
        )

        self.title, self.items = self.extract(tree, bridge)

    # Apply `xpath` to `element` and retrieve one result. The result is
    # converted to a string if needed. Returns `default` if it is set and no
    # result were retrieved.
    @classmethod
    def xpathout(cls, element, xpath, default = None):
        result = element.xpath(xpath)
        if (not result) and (default is not None):
            result = default
        else:
            result = result[0]

        if isinstance(result, lxml.html.HtmlElement):
            return lxml.etree.tostring(result, encoding = "unicode")
        else:
            return result

    # Convert all urls from the HTML `tree` to absolute ones by combining them
    # with `base`.
    @classmethod
    def urlabs(cls, tree, base):
        for element in tree.xpath('//*[@src]'):
            url = urljoin(base, element.get('src'))
            element.set('src', url)
        for element in tree.xpath('//*[@href]'):
            url = urljoin(base, element.get('href'))
            element.set('href', url)

    # Extract elements needed to create a feed from the HTML `tree`. Elements
    # are extracted using XPath expressions defined in `bridge`. Return the
    # feed title and its items.
    @classmethod
    def extract(cls, tree, bridge):
        title = " ".join( cls.xpathout(tree, "//title/text()").split() )

        items = []
        for element in tree.xpath(bridge.rootxp):
            item = Table()
            item.title = cls.xpathout(element, bridge.titlexp)
            item.url = cls.xpathout(element, bridge.urlxp)
            item.updated = datetime.strptime(
                cls.xpathout(element, bridge.datexp),
                bridge.datefmt,
            )
            item.id = f"{item.url}/{item.updated.isoformat()}"
            if bridge.idxp:
                extraid = cls.xpathout(element, bridge.idxp, default = '')
                item.id += f"/{extraid}"
            if bridge.descxp:
                item.summary = cls.xpathout(element, bridge.descxp)
            items.append(item)

        if bridge.reverse: items = items[::-1]

        return title, items

flaskapp = flask.Flask(__name__)

@flaskapp.route('/feed')
def feed():
    xpathfeed = XPathFeed(flask.request.args["src"])
    feed = AtomFeed(
        title = xpathfeed.title,
        url   = xpathfeed.source_url,
        id    = xpathfeed.source_url,
    )
    for i in xpathfeed.items: feed.add(**i)
    return feed.get_response()

@flaskapp.route('/preview')
def preview():
    xpathfeed = XPathFeed(flask.request.args["src"])
    return flask.render_template("preview.html",
        title = xpathfeed.title,
        url   = xpathfeed.source_url,
        items = xpathfeed.items,
    )
