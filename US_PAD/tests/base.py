# import warnings
from django import setup
import os
from django.test.utils import setup_test_environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "US_PAD.settings")
setup()
from dotenv import load_dotenv

load_dotenv()
from django.test import TestCase, Client


class SetUp(TestCase):
    setup_test_environment()

    def setUp(self):
        # warnings.simplefilter("ignore", category=ResourceWarning)
        self.client = Client()
