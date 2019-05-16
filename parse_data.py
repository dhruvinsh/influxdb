def _dict_to_line(dikt: dict) -> str:
    return ','.join(['{}={}'.format(k, v) for k, v in dikt.items()])


def make_line(data: dict) -> str:
    """allows to make line out of json
    data = {
        'measurement': 'cpu',
        'tags': {'hostname': 'localhost', 'region': 'ca'},
        'fields': {'value': 0.51}
    }
    ==> cpu,hostname=localhost,region=ca value=0.51
    """
    query = ''
    measurement = data.get("measurement")
    tags = data.get("tags")
    fields = data.get("fields")

    assert measurement is not None, "Should need to have measurement"
    assert fields is not None, "Should need to have fields"
    query += measurement

    if tags:
        query += ',' + _dict_to_line(tags)

    if fields:
        query += ' ' + _dict_to_line(fields)

    return query
