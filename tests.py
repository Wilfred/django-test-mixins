from unittest import main
from mock import Mock

# set up dummy settings
# this needs to happen before we import django_test_mixins
from django.conf import settings
settings.configure(DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }
})

from django_test_mixins import HttpCodeTestCase

class AssertionTest(HttpCodeTestCase):
    def test_http_ok(self):
        self.assertHttpOK(Mock(status_code=200))

        with self.assertRaises(AssertionError):
            self.assertHttpOK(Mock(status_code=404))

    def test_http_bad_request(self):
        self.assertHttpBadRequest(Mock(status_code=400))

        with self.assertRaises(AssertionError):
            self.assertHttpBadRequest(Mock(status_code=200))

    def test_http_not_found(self):
        self.assertHttpNotFound(Mock(status_code=404))

        with self.assertRaises(AssertionError):
            self.assertHttpNotFound(Mock(status_code=200))

    def test_http_redirect(self):
        self.assertHttpRedirect(Mock(status_code=301))
        self.assertHttpRedirect(Mock(status_code=302))

        with self.assertRaises(AssertionError):
            self.assertHttpRedirect(Mock(status_code=200))


if __name__ == '__main__':
    main()
