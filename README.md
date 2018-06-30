# django-test-mixins

Additional assertions and test conveniences for testing django
sites.

[![Build Status](https://travis-ci.org/Wilfred/django-test-mixins.svg)](https://travis-ci.org/Wilfred/django-test-mixins)
[![Coverage Status](https://img.shields.io/coveralls/Wilfred/django-test-mixins.svg)](https://coveralls.io/r/Wilfred/django-test-mixins)
[![Latest Version](https://img.shields.io/pypi/v/django_test_mixins.svg)](https://pypi.python.org/pypi/django_test_mixins/)
[![Downloads](https://img.shields.io/pypi/dm/django_test_mixins.svg)](https://pypi.python.org/pypi/django_test_mixins/)
[![License](https://img.shields.io/pypi/l/django_test_mixins.svg)](https://pypi.python.org/pypi/django_test_mixins/)

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [django-test-mixins](#django-test-mixins)
    - [Usage](#usage)
        - [HttpCodeTestCase](#httpcodetestcase)
        - [EmptyCacheTestCase](#emptycachetestcase)
        - [FormValidationTestCase](#formvalidationtestcase)
        - [RedirectTestCase](#redirecttestcase)
        - [Combining test cases](#combining-test-cases)
    - [Uploading to PyPI](#uploading-to-pypi)

<!-- markdown-toc end -->

## Usage

All classes inherit from
[django.test.TestCase](https://docs.djangoproject.com/en/dev/topics/testing/overview/#django.test.TestCase)
so you can access the Django assertions and the HTTP client as usual.

django-test-mixins is
[available on PyPI](https://pypi.python.org/pypi/django_test_mixins). Installation
is simply a matter of:

    $ pip install django_test_mixins

### HttpCodeTestCase

`HttpCodeTestCase` provides the following assertions for exact HTTP responses:

* `assertHttpOK(response)` (200)
* `assertHttpCreated(response)` (201)
* `assertHttpBadRequest(response)` (400)
* `assertHttpUnauthorized(response)` (401)
* `assertHttpForbidden(response)` (403)
* `assertHttpNotFound(response)` (404)
* `assertHttpMethodNotAllowed(response)` (405)

It also provides the following assertions for groups of HTTP
responses:

* `assertHttpRedirect(response, location=None)` (3XX)

Example:

```python
from django.core.urlresolvers import reverse

from django_test_mixins import HttpCodeTestCase


class TestIndex(HttpCodeTestCase):
    def test_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertHttpOK(response)
```

### EmptyCacheTestCase

`EmptyCacheTestCase` provides no extra assertions, but ensures that
every test starts with a empty cache.

### FormValidationTestCase

`FormValidationTestCase` provides the following assertion:

* `assertFormInvalid(response, form_name="form")`

Example:

Assume we have a view that looks like this:

```python
from django.shortcuts import render, redirect

from .forms import HouseForm


def create_house(request):
    if request.method == 'POST':
        form = HouseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = HouseForm()

    return render(request, "create_house.html", {'house_form': form})
```

We can then write a test like this. Note that `form_name` needs to
match the context we rendered the page with (defaults to `"form"`).

```python
from django.core.urlresolvers import reverse

from django_test_mixins import FormValidationTestCase


class TestCreateHouse(FormValidationTestCase):
    def test_create_requires_name(self):
        response = self.client.post(reverse('create_house'), {})
        self.assertFormInvalid(response, form_name="house_form")
```

### RedirectTestCase

`RedirectTestCase` provides the following assertions:

* `assertRedirectsTo(response, expected_url)`

Django has `TestCase.assertRedirects`
([docs](https://docs.djangoproject.com/en/dev/topics/testing/overview/#django.test.SimpleTestCase.assertRedirects))
but this does not support redirects to external URLs because of
limitations in the test client.

`assertRedirectsTo` does not support chained redirects, so you can't
do `self.client.get(SOME_URL, follow=True)`.

Example:

```python
from django.core.urlresolvers import reverse

from django_test_mixins import FormValidationTestCase


class TestIndex(RedirectTestCase):
    def test_home_redirects_to_login(self):
        """If the user isn't logged in, index should redirect to the login page.

        """
        response = self.client.get(reverse('index'))
        self.assertRedirectsTo(response, reverse('log_in'))
```


### Combining test cases

You can freely combine these classes by simply inheriting from
multiple classes.

```python
from django.core.urlresolvers import reverse

from django_test_mixins import FreshCacheTestCase, HttpCodeTestCase


class TestIndex(FreshCacheTestCase, HttpCodeTestCase):
    def test_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertHttpOK(response)
```

## Uploading to PyPI

Releasing a new version is a matter of:

    $ python setup.py sdist upload
