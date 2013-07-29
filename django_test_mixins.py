from django.test import TestCase
from django.core.cache import cache


class EmptyCacheTestCase(TestCase):
    """Ensure that every test starts with an empty cache."""
    def setUp(self):
        super(EmptyCacheTestCase, self).setUp()
        cache.clear()
