from .base import BaseFeed
from .aemet import AemetFeed
from .cofg import CofgFeed
from .gipuzkoa_gao import GipuzkoaGaoFeed
from .gipuzkoa_tides import GipuzkoaTidesFeed
from .kosta import KostaFeed
from .magicseaweed import MagicseaweedFeed
from .overpass import OverpassFeed


__all__ = [
    'BaseFeed',
    'AemetFeed',
    'CofgFeed',
    'GipuzkoaGaoFeed',
    'GipuzkoaTidesFeed',
    'KostaFeed',
    'MagicseaweedFeed',
    'OverpassFeed',
]
