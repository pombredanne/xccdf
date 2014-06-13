from xccdf.models import tests


def suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTests(tests.suite())
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
