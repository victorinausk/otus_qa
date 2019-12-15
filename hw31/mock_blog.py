# -*- coding: UTF-8 -*-
"""Базовый вывод постов блога"""
import requests


class Blog:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def posts():
        response = requests.get("https://jsonplaceholder.typicode.com/posts")

        return response.json()

    def __repr__(self):
        return '<Blog: {}>'.format(self.name)
