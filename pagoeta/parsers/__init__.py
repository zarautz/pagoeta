from .base import BaseParser

from .aemet import AemetParser
from .cofg import CofgParser
from .ingurumena import IngurumenaTidesParser
from .kosta import KostaParser
from .magicseaweed import MagicseaweedParser
from .overpass import OverpassParser
from .turismo import TurismoAgendaParser, TurismoEventParser


__all__ = [
    'BaseParser',
    'AemetParser',
    'CofgParser',
    'IngurumenaTidesParser',
    'KostaParser',
    'MagicseaweedParser',
    'OverpassParser',
    'TurismoAgendaParser',
    'TurismoEventParser',
]
