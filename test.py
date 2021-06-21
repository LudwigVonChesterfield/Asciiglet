import sys
import unittest

import tests.test_examples


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('../tests', 'test_*.py')

    runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)

    result = runner.run(suite)

    sys.exit(not result.wasSuccessful())
