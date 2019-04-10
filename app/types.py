import typing
from dataclasses import dataclass

class Table(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

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
