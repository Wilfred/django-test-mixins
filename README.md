# django-test-mixins

Additional assertions and test conveniences for testing django
sites. MIT license.

## Features

* `HttpTestCase` mixin provides `assertHttpOK`, `assertHttpNotFound`
  etc instead of writing `assertEqual(response.status_code, 200)`, and
  a redirect assertion that supports external URLs.
* Empty cache test mixin, to start from afresh every time

## Future Features

* Example usage
* PEP 8 assertion mixin
* Form validation mixin
