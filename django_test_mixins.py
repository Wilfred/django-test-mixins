from django.test import TestCase
from django.core.cache import cache

import urlparse


class HttpCodeTestCase(TestCase):
    # TODO: this should be a private method.
    def assertHttpCode(self, response, code, code_description):
        self.assertEqual(
            response.status_code, code,
            "Expected an HTTP %s (%s) response, but got HTTP %s" %
            (code, code_description, response.status_code))

    def assertHttpOK(self, response):
        self.assertHttpCode(response, 200, "OK")

    def assertHttpCreated(self, response):
        self.assertHttpCode(response, 201, "Created")

    def assertHttpRedirect(self, response, location=None):
        """Assert that we had any redirect status code.

        """
        self.assertTrue(
            300 <= response.status_code < 400,
            "Expected an HTTP 3XX (redirect) response, but got HTTP %s" %
            response.status_code
        )

        if location:
            if location.startswith("http://testserver/"):
                absolute_location = location
            else:
                absolute_location = urlparse.urljoin("http://testserver/",  location)

            self.assertEqual(response['Location'], absolute_location)


    def assertHttpBadRequest(self, response):
        self.assertHttpCode(response, 400, "Bad Request")

    def assertHttpUnauthorized(self, response):
        self.assertHttpCode(response, 401, "Unauthorized")

    def assertHttpForbidden(self, response):
        self.assertHttpCode(response, 403, "Forbidden")

    def assertHttpNotFound(self, response):
        self.assertHttpCode(response, 404, "Not Found")

    def assertHttpMethodNotAllowed(self, response):
        self.assertHttpCode(response, 405, "Method Not Allowed")


class EmptyCacheTestCase(TestCase):
    """Ensure that every test starts with an empty cache."""
    def setUp(self):
        super(EmptyCacheTestCase, self).setUp()
        cache.clear()


class FormValidationTestCase(TestCase):
    def assertFormInvalid(self, response, form_name="form"):
        """Assert that the response contains a form in the context, and that
        the form failed validation. The form is assumed to be in
        context[form_name].

        If the form has validated when it shouldn't, views often
        redirect somewhere, so we also check for HTTP 200.

        """
        form = None
        try:
            if response.context:
                form = response.context[form_name]
        except KeyError:
            pass

        if not form:
            self.fail("Could not find a form in the response.")

        self.assertFalse(form.is_valid(), "Expected form to be invalid, but it was valid.")

        status_code = response.status_code
        self.assertEqual(
            status_code, 200,
            "Expected HTTP 200, but got HTTP %d. "
            "Looks like the form validated when it shouldn't." % status_code)


class RedirectTestCase(TestCase):
    def assertRedirectsTo(self, response, expected_url):
        """Django's assertRedirects doesn't support external URLs, so we roll
        our own here. Note that the test client can't fetch external
        URLs, so we mustn't use fetch=True.

        """
        if response.status_code != 302:
            self.fail("Did not redirect (got HTTP %s instead)." % response.status_code)

        if hasattr(response, "redirect_chain"):
            self.fail("You can't use assertRedirects with follow=True.")

        final_url = response._headers['location'][1]

        if not expected_url.startswith('http://') and not expected_url.startswith('https://'):
            # we were given a relative URL, so convert it
            expected_url = "http://testserver%s" % expected_url

        self.assertEqual(
            final_url, expected_url,
            "Expected to be redirected to %s, but got %s instead." % (expected_url, final_url)
        )
