""" API tests for https://dog.ceo/dog-api/ """
# -*- coding: UTF-8 -*-

import pytest

ENDPOINTS = [
    '/breeds/list/all',
    '/breeds/image/random',
    '/breeds/image/random/10',
    '/breed/african/images',
    '/breed/african/images/random/10',
    '/breed/collie/list',
    '/breed/collie/images',
    '/breed/collie/border/images/random',
    '/breed/collie/border/images/random/10',
]

@pytest.mark.parametrize('endpoint', ENDPOINTS)
def test_dogapi(dogceo, endpoint):
    """ Test GET requests for https://dog.ceo/api """
    response = dogceo.do_get(endpoint)
    print(response)
    assert response.status_code == 200
    assert response.reason == 'OK'
    assert response.headers['Content-Type'] == 'application/json'
