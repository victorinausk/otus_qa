# -*- coding: UTF-8 -*-
"""Подмена постов блога"""

from unittest import TestCase
from unittest.mock import patch

from .mock_blog import Blog


class TestBlog(TestCase):
    @patch('hw31.mock_blog.Blog')
    def test_blog_posts(self, mockblog):
        blog = mockblog()

        blog.posts.return_value = [
            {
                'userId': 1,
                'id': 1,
                'title': 'Test Title',
                'body': 'Far out in the uncharted backwaters of the unfashionable end of the western spiral arm '
                        'of the Galaxy\n lies a small unregarded yellow sun.'
            }
        ]

        response = blog.posts()
        self.assertIsNotNone(response)
        self.assertIsInstance(response[0], dict)

        assert mockblog is not Blog  # The mock is not equivalent to the original

        assert mockblog.called  # The mock was called

        blog.posts.assert_called_with()  # We called the posts method with no arguments

        blog.posts.assert_called_once_with()  # We called the posts method once with no arguments

        # blog.posts.assert_called_with(1, 2, 3) - This assertion is False and will fail since we called blog.posts with no arguments

        blog.reset_mock()  # Reset the mock object

        blog.posts.assert_not_called()  # After resetting, posts has not been called.
