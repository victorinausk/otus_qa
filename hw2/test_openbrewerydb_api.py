""" API tests for https://www.openbrewerydb.org/ """
# -*- coding: UTF-8 -*-

import pytest

ENDPOINTS = [
    '/breweries',
    '/breweries?by_state=maine',
    '/breweries?by_state=california&by_type=brewpub',
    '/breweries?per_page=10&page=17',
    '/breweries/autocomplete?query=wolf',
    '/breweries?by_name=brew',
    '/breweries?by_city=chicago&sort='
    '/breweries?by_city=miami&sort=+type&per_page=10&page=1',
    '/breweries/5494',
    '/breweries?by_state=ohio&sort=type,-name',
]

@pytest.mark.parametrize('endpoint', ENDPOINTS)
def test_brewery(openbrewery, endpoint):
    """ Test GET requests for https://api.openbrewerydb.org """
    response = openbrewery.do_get(endpoint)
    print(response)
    assert response.status_code == 200
    assert response.reason == 'OK'
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8'
