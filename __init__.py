"""A python wrpper to Influxdb database

Author: Dhruvin Shah


* Changelogs:
v1.0 - Initial release with basic support like inserting data
v1.1 - DataFactory added for easy and predictable data creation"""

from .connector import InfluxdbClient
from .factory import DataFactory

__version__ = 1.1

__all__ = ['InfluxdbClient', 'DataFactory']
