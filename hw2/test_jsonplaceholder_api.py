""" API tests for https://jsonplaceholder.typicode.com/ """
# -*- coding: UTF-8 -*-

import pytest

ENDPOINTS = [
    '/todos/1',
    '/posts/1/comments',
    '/comments?postId=1',
    '/posts?userId=1',
    '/albums',
    '/albums/1',

]


@pytest.mark.parametrize('endpoint', ENDPOINTS)
def test_jph(jph, endpoint, module_fixture):
    """ Test GET requests for https://api.openbrewerydb.org """
    response = jph.do_get(endpoint)
    print(response)
    assert response.status_code == 200
    assert response.reason == 'OK'
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8'
