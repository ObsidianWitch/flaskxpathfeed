import re

from app.table import Table

bridges = Table(
    ao3_search = Table(
        match     = lambda url: "archiveofourown.org/works?" in url,
        rootxp    = "//ol[@class = 'work index group']/li",
        extraidxp = "dl/dd[@class = 'chapters']/text()",
        titlexp   = "div/h4/a/text()",
        urlxp     = "div/h4/a/@href",
        descxp    = ".",
        datexp    = "div/p[@class = 'datetime']/text()",
        datefmt   = "%d %b %Y",
    ),
    ao3_work = Table(
        match   = lambda url: re.search(
            pattern = re.escape("archiveofourown.org/works/")
                + "[0-9]+"
                + re.escape("/navigate"),
            string = url,
        ),
        rootxp  = "//ol[@class = 'chapter index group']/li",
        titlexp = "a/text()",
        urlxp   = "a/@href",
        datexp  = "span[@class = 'datetime']/text()",
        datefmt = "(%Y-%m-%d)",
    ),
)
