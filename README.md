**Table of Contents**  *generated with [DocToc](http://doctoc.herokuapp.com/)*

- [django-test-mixins](#django-test-mixins)
	- [Usage](#usage)
		- [HttpCodeTestCase](#httpcodetestcase)
		- [EmptyCacheTestCase](#emptycachetestcase)
		- [FormValidationTestCase](#formvalidationtestcase)
		- [Combining test cases](#combining-test-cases)
	- [Changelog](#changelog)
		- [v1.0](#v10)
	- [Future Features](#future-features)

# django-test-mixins

Additional assertions and test conveniences for testing django
sites. MIT license.

## Usage

All classes inherit from
[django.test.TestCase](https://docs.djangoproject.com/en/dev/topics/testing/overview/#django.test.TestCase)
so you can access the Django assertions and the HTTP client as usual.

Installation is simply a matter of:

    $ pip install django_test_mixins

### HttpCodeTestCase

`HttpCodeTestCase` provides the following assertions:

* `assertHttpOK(response)`
* `assertHttpBadRequest(response)`
* `assertHttpForbidden(response)`
* `assertHttpNotFound(response)`

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

## Changelog

### v1.0

Initial release.

## Future Features

* PEP 8 assertion mixin
