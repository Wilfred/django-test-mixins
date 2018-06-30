## v1.11

Added Python 3 support.

Tags 1.11.1 and 1.11.2 contain the same code, but were created due to
problems releasing from Travis.

## v1.10

Fixed a bug with `.assertRedirectsTo` where absolute HTTPS URLs were
treated as relative URLs.

## v1.9

Fixed a bug where the `form_name` argument to `assertFormInvalid` was
being ignored.

## v1.8

`HttpCodeTestCase.assertHttpRedirect` can now take a `location`
argument for verifying that redirects go to a specific path.

## v1.7.1

Minor spelling fix in assertion message.

## v1.7

Added `HttpCodeTestCase.assertHttpRedirect`

## v1.6

Added `HttpCodeTestCase.assertHttpUnauthorized`

## v1.5

Added `HttpCodeTestCase.assertHttpMethodNotAllowed`

## v1.4

Added `HttpCodeTestCase.assertHttpCreated`

## v1.3

Added `RedirectTestCase`.

## v1.2

Fixed a crash on `HttpCodeTestCase` assertions when the assertion
failed.

## v1.1

Fixed `HttpCodeTestCase` assertions which were throwing
`AttributeError`.

## v1.0

Initial release.
