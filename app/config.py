from app.table import Table

bridges = Table(
    ao3_search = Table(
        rootxp  = "//ol[@class = 'work index group']/li",
        titlexp = "div/h4/a",
        urlxp   = "div/h4/a/@href",
        descxp  = "",
        datexp  = "div/p[@class = 'datetime']",
        datefmt = "%d %b %Y",
    ),
    ao3_work = Table(
        rootxp  = "//ol[@class = 'chapter index group']/li",
        titlexp = "a",
        urlxp   = "a/@href",
        datexp  = "span[@class = 'datetime']",
        datefmt = "(%Y-%m-%d)",
    ),
)
