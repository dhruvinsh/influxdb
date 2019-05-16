import requests

from .logging import logger
from .parse_data import make_line


class InfluxdbClient(object):
    "A client for Influxdb"

    def __init__(self, host, port: int=8086, ssl: bool=False):
        """An influxdb client"""
        self.host = host
        self.port = port
        self.protocol = 'https' if ssl else 'http'
        self.session = requests.session()

        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount(self.protocol + '://', adapter)
        self._database = None

    @property
    def database(self):
        "get database"
        return self._database

    @database.setter
    def database(self, db: str):
        self._database = db

    def close(self):
        "close http session"
        if isinstance(self.session, requests.Session):
            self.session.close()

    def make_requests(self, method: str, url: str, **kwargs):
        """factory function for requests
        TODO: need to work on below output,
        response when database getting created
        {"results":[{"statement_id":0}]}
        """
        logger.debug("""Making requests to : %s parameters are: %s""" %(url, kwargs))
        resp = self.session.request(method=method, url=url, **kwargs)

        err = False
        if resp.content:
            err = resp.json().get('error')

        if err:
            raise ValueError(err)
        return resp.content

    def query_url(self, url: str) -> str:
        "url generator"
        assert url in ['write', 'query'], "parameter only be 'write' or 'query'"
        return f'{self.protocol}://{self.host}:{self.port}/{url}'

    def create_database(self, db: str):
        "create database"
        url = self.query_url('query')
        payload = {'q': f'CREATE DATABASE {db}'}

        return self.make_requests('post', url, params=payload)

    def insert_data(self, data: dict, database: str=None):
        "allows to make entry"
        url = self.query_url('write')
        payload = {'db': database or self.database}
        data = make_line(data)

        return self.make_requests('post', url, params=payload, data=data)
