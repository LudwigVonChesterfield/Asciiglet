import unittest
import asciiglet
import pkgutil
import importlib
import sys
import io

from parameterized import parameterized


def get_tests():
    for loader, name, is_pkg in pkgutil.walk_packages(
        asciiglet.examples.__path__
    ):
        yield name, loader, is_pkg


class ExamplesTests(unittest.TestCase):
    @parameterized.expand(
        [test for test in get_tests()]
    )
    def test_should_not_crash_immediatley(self, name, loader, is_pkg):
        full_name = asciiglet.examples.__name__ + '.' + name
        module = importlib.import_module(full_name)

        module.environment.run(halt_after=10)
