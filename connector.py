from dataclasses import dataclass, field

import requests

from .logging import logger
from .parse_data import make_line


@dataclass
class InfluxdbClient(object):
    "A client for Influxdb"

    host: str
    port: int = 8086
    ssl: bool = False
    _database: str = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self.protocol = 'https' if self.ssl else 'http'
        self.session = requests.session()

        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount(self.protocol + '://', adapter)

    @property
    def database(self) -> str:
        """get current selected database"""
        return self._database

    @database.setter
    def database(self, db: str) -> None:
        """set new database as current working database"""
        self._database = db

    def close(self) -> None:
        """close requests http session"""
        if isinstance(self.session, requests.Session):
            self.session.close()

    def make_requests(self, method: str, url: str, **kwargs):
        """factory function for requests
        TODO: need to work on below output,
        response when database getting created
        {"results":[{"statement_id":0}]}
        """
        logger.debug("""Making requests to : %s parameters are: %s""" %
                     (url, kwargs))
        resp = self.session.request(method=method, url=url, **kwargs)

        err = False
        if resp.content:
            err = resp.json().get('error')

        if err:
            raise ValueError(err)
        return resp.content

    def get_url(self, url: str) -> str:
        """url generator with 'write' or 'query' append to default
        url based on choosen functionality.

        for more detail see official documents of influxdb"""
        assert url in ['write',
                       'query'], "parameter can only be 'write' or 'query'"
        return f'{self.protocol}://{self.host}:{self.port}/{url}'

    def create_database(self, db: str):
        """allow to create database"""
        url = self.get_url('query')
        payload = {'q': f'CREATE DATABASE {db}'}

        return self.make_requests('post', url, params=payload)

    def insert_data(self, data: dict, database: str = None):
        """allows to make entry in to selected database

        param: data: a dictionary where has 3 key-pair value,
                     one is measurement: None,
                     second is tags: {}
                     third is fields: {}
               database: to override default selected database

        for example, data looks like as below:
        data = {
            'measurement': 'cpu',
            'tags': {'hostname': 'localhost', 'region': 'ca'},
            'fields': {'value': 0.51}
        }
        """
        url = self.get_url('write')
        payload = {'db': database or self.database}
        data = make_line(data)

        return self.make_requests('post', url, params=payload, data=data)
