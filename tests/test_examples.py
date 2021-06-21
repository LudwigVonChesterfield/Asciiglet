import unittest
import asciiglet
import pkgutil
import importlib


class ExamplesDontCrash(unittest.TestCase):
    def test_examples(self):
        for loader, name, is_pkg in pkgutil.walk_packages(
            asciiglet.examples.__path__
        ):
            full_name = asciiglet.examples.__name__ + '.' + name
            module = importlib.import_module(full_name)

            module.environment.run(halt_after=10)
