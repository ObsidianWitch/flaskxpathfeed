import re
import typing
from dataclasses import dataclass

from app.types import Table

@dataclass
class Bridge:
    match   : typing.Callable
    rootxp  : str
    titlexp : str
    urlxp   : str
    datexp  : str
    datefmt : str
    idxp    : str = None
    descxp  : str = None
    reverse : bool = False

table = Table(
    ao3_work = Bridge(
        match   = lambda url: re.search(
            pattern = re.escape("archiveofourown.org/works/")
                + "[0-9]+"
                + re.escape("/navigate"),
            string = url,
        ),
        reverse = True,
        rootxp  = "//ol[@class = 'chapter index group']/li",
        titlexp = "a/text()",
        urlxp   = "a/@href",
        datexp  = "span[@class = 'datetime']/text()",
        datefmt = "(%Y-%m-%d)",
    ),
    ao3_list = Bridge(
        match   = lambda url: (
            "archiveofourown.org/works" in url
            or "https://archiveofourown.org/bookmarks" in url
        ),
        rootxp  = "//ol[contains(@class, 'index group')]/li",
        idxp    = "dl/dd[@class = 'chapters']/text()",
        titlexp = "div/h4/a/text()",
        urlxp   = "div/h4/a/@href",
        descxp  = ".",
        datexp  = "div/p[@class = 'datetime']/text()",
        datefmt = "%d %b %Y",
    ),
)
