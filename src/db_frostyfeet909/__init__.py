"""Provides my own methods to work with a queue pool from SQL alchemy with raw-ish SQL.

The module and any `Connection` object may be import or instantiated any number of times across the program but will use the same
engine/pool when given the same URL.

documentation: https://github.com/frostyfeet909/db_frostyfeet909
"""


__author__ = "Algernon Sampson (algiesampson@gmail.com)"
__version__ = "1.0.0"
__license__ = "GNU General Public License v3.0"


from .main import Connection
