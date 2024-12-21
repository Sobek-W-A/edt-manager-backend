import unittest

if __name__ == "__main__":

    loader = unittest.TestLoader().discover("./tests")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(loader)

