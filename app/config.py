from app.table import Table

ao3_search = Table(
    rootxp  = "//ol[@class = 'work index group']/li",
    titlexp = "div/h4/a",
    urlxp   = "div/h4/a/@href",
    descxp  = "",
    datexp  = "div/p[@class = 'datetime']",
    datefmt = "%d %b %Y",
)

ao3_work = Table(
    rootxp  = "//ol[@class = 'chapter index group']/li",
    titlexp = "a",
    urlxp   = "a/@href",
    datexp  = "span[@class = 'datetime']",
    datefmt = "(%Y-%m-%d)",
)

config = Table(
    ao3_madokaff = Table(
        title   = "AO3 - Madoka Magica, F/F",
        src     = "https://frama.link/P8vbNj2N",
        **ao3_search,
    ),

    ao3_deluge = Table(
        title   = "AO3 - Deluge",
        src     = "https://archiveofourown.org/works/3584145/navigate",
        **ao3_work,
    ),
)
