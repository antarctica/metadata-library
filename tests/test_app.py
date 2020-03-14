from http import HTTPStatus

from flask import current_app

from tests.test_base import BaseTestCase


class AppTestCase(BaseTestCase):
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_app_response(self):
        response = self.client.get(
            '/',
            base_url='http://localhost:9000'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.mimetype, 'application/json')
        expected_response = {'meta': 'Root endpoint for Metadata Generator internal API'}
        self.assertDictEqual(response.json, expected_response)
