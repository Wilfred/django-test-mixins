from django.test import TestCase
from django.core.cache import cache


class HttpCodeTestCase(TestCase):
    def assertHttpCode(self, response, code, code_description):
        self.assertEqual(
            response.status_code, code,
            "Expected an HTTP %s (%s) response, but got HTTP %s" %
            code, code_description, response.status_code)

    def assertHttpOK(self, response):
        self.assertExpectHttpCode(response, 200, "OK")

    def assertHttpBadRequest(self, response):
        self.assertExpectHttpCode(response, 400, "Bad Request")

    def assertHttpForbidden(self, response):
        self.assertExpectHttpCode(response, 403, "Forbidden")

    def assertHttpNotFound(self, response):
        self.assertExpectHttpCode(response, 404, "Not Found")


class EmptyCacheTestCase(TestCase):
    """Ensure that every test starts with an empty cache."""
    def setUp(self):
        super(EmptyCacheTestCase, self).setUp()
        cache.clear()
