from django.test import TestCase

class ExampleTestCase(TestCase):
    is_setup = False
    def setUp(self):
        self.is_setup = True

    def (self):
        self.assertTrue(self.is_setup)