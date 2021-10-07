import os

from django.test import TestCase, TransactionTestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

TestCase.databases = ["default"]
TransactionTestCase.databases = ["default"]
