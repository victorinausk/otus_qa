""" API tests for https://dog.ceo/dog-api/ """
# -*- coding: UTF-8 -*-

import pytest
import requests

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


@pytest.mark.parametrize("test_input", ["terrier", "pointer", "hound", "spaniel"])
class TestWithBreed:
    # pylint: disable=too-few-public-methods
    """ Test GET requests for https://dog.ceo/api """

    @classmethod
    def test_img_by_breed(cls, test_input):
        """
        Проверка соответствия выборки изображений согласно породе ..
        :param test_input:
        """
        url = "https://dog.ceo/api/breed/" + test_input + "/images"
        r = requests.get(url)
        img = r.json()['message']
        errors = 0
        for i in img:
            if test_input not in i:
                print(test_input + " == " + i)
                errors += 1
        assert errors == 0
