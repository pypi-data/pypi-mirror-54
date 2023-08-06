"""Datasetmaker clients."""

from .esv import ESVClient
from .hdi import HDIClient
from .meps import MEPs
from .mynewsflash.client import MyNewsFlashClient
from .nobel import NobelClient
from .scb import SCBClient
from .sipri import SIPRI
from .skolverket.client import SkolverketClient
from .unsc import UNSC
from .valforsk import ValforskClient
from .waqi import WAQIClient
from .wikipedia.client import WikipediaClient
from .worldbank import WorldBank


available = {
    # 'oecd': OECD,
    # 'socialstyrelsen': SocialstyrelsenClient,
    'esv': ESVClient,
    'hdi': HDIClient,
    'meps': MEPs,
    'mynewsflash': MyNewsFlashClient,
    'nobel': NobelClient,
    'scb': SCBClient,
    'sipri': SIPRI,
    'skolverket': SkolverketClient,
    'unsc': UNSC,
    'valforsk': ValforskClient,
    'waqi': WAQIClient,
    'wikipedia': WikipediaClient,
    'worldbank': WorldBank,
}
