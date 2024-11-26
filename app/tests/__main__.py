import unittest

if __name__ == "__main__":

    loader = unittest.TestLoader().discover("./app/tests/routes")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(loader)

