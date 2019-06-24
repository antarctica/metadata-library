from http import HTTPStatus

from flask import current_app

from tests.test_base import BaseTestCase


class AppTestCase(BaseTestCase):
    @unittest.skip
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_app_response(self):
        response = self.client.get(
            '/',
            base_url='http://localhost:9000'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.mimetype, 'application/json')
        expected_response = {'meta': 'root endpoint for Metadata Generator internal app'}
        self.assertDictEqual(response.json, expected_response)
