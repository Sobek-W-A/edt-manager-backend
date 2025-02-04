"""
main file to execute the test suite
"""

from unittest import TestLoader, TestSuite, TextTestRunner

if __name__ == "__main__":

    loader: TestSuite = TestLoader().discover("./tests")
    runner: TextTestRunner = TextTestRunner(verbosity=2)
    runner.run(loader)
