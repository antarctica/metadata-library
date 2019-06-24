
from flask import current_app

from tests.test_base import BaseTestCase


class AppTestCase(BaseTestCase):
    @unittest.skip
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
