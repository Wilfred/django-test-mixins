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

from django_test_mixins import HttpCodeTestCase, FormValidationTestCase

class HttpAssertionsTest(HttpCodeTestCase):
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


class FormAssertionsTest(FormValidationTestCase):
    def test_form_invalid(self):
        """If we have a request containing a form with .is_valid returning
        False, then the form was indeed invalid.

        """
        mock_form = Mock()
        mock_form.is_valid.return_value = False
        
        mock_request = Mock(context={'form': mock_form}, status_code=200)
        self.assertFormInvalid(mock_request)

    def test_form_invalid_fails_on_redirect(self):
        """If the form was valid, the most common scenario is that we were
        redirected and there's no form present.

        """
        mock_request = Mock(status_code=302, context={})

        with self.assertRaises(AssertionError):
            self.assertFormInvalid(mock_request)


if __name__ == '__main__':
    main()
