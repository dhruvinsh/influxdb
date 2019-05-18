"""
influxdb key concept, there are 3 components: measurement, tags, fields

measurement and fields are medetory, and tags are not. measurement will have
only one value, whereas fields might have more than one. one value is must.

python client is rest api for influxdb. and data insertion works based on
making post request where payload is string. this client converts python
dict object to string


example:
python data object:
    data = {
        'measurement': 'cpu',
        'tags': {'hostname': 'localhost', 'region': 'ca'},
        'fields': {'value': 0.51}
    }

converting to string:
    ==> cpu,hostname=localhost,region=ca value=0.51
        "m",".........tags............." "..fields.."
                                        ^
                                        |
                                        --- space between tags and fields
"""

from dataclasses import dataclass


@dataclass
class DataFactory(object):

    measurement: str
    fields: dict
    tags: dict = None

    @property
    def data(self) -> dict:
        "factory data generator as dict"
        if self.tags is None:
            return {'measurement': self.measurement,
                    'fields': self.fields}

        return {'measurement': self.measurement,
                'tags': self.tags,
                'fields': self.fields}
