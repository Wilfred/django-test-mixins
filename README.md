# django-test-mixins

Additional assertions and test conveniences for testing django
sites. MIT license.

## Usage

All classes inherit from
[django.test.TestCase](https://docs.djangoproject.com/en/dev/topics/testing/overview/#django.test.TestCase)
so you can access the Django assertions and the HTTP client as usual.

### HttpTestCase

`HttpCodeTestCase` provides the following assertions:

* `assertHttpOK(response)`
* `assertHttpBadRequest(response)`
* `assertHttpForbidden(response)`
* `assertHttpNotFound(response)`

Example:

    from django.core.urlresolvers import reverse

    from django_test_mixins import HttpCodeTestCase


    class TestIndex(HttpCodeTestCase):
        def test_home_page(self):
            response = self.client.get(reverse('index'))
            self.assertHttpOK(response)

### EmptyCacheTestCase

`EmptyCacheTestCase` provides no extra assertions, but ensures that
every test starts with a empty cache.

### Combining test cases

You can freely combine these classes by simply inheriting from
multiple classes.

    from django.core.urlresolvers import reverse

    from django_test_mixins import FreshCacheTestCase, HttpCodeTestCase


    class TestIndex(FreshCacheTestCase, HttpCodeTestCase):
        def test_home_page(self):
            response = self.client.get(reverse('index'))
            self.assertHttpOK(response)

## Future Features

* PEP 8 assertion mixin
* Form validation mixin
