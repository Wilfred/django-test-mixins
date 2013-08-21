from django.test import TestCase
from django.core.cache import cache


class HttpCodeTestCase(TestCase):
    def assertHttpCode(self, response, code, code_description):
        self.assertEqual(
            response.status_code, code,
            "Expected an HTTP %s (%s) response, but got HTTP %s" %
            code, code_description, response.status_code)

    def assertHttpOK(self, response):
        self.assertHttpCode(response, 200, "OK")

    def assertHttpBadRequest(self, response):
        self.assertHttpCode(response, 400, "Bad Request")

    def assertHttpForbidden(self, response):
        self.assertHttpCode(response, 403, "Forbidden")

    def assertHttpNotFound(self, response):
        self.assertHttpCode(response, 404, "Not Found")


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
                form = response.context['form']
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

