import unittest
from evalgate import evaluate
class GateTest(unittest.TestCase):
    def test_regression(self):
        report=evaluate('candidate')
        self.assertGreater(report['candidate']['accuracy'],report['baseline']['accuracy'])
        self.assertEqual(sum(r['status']=='block' for r in report['slices']),1)
        self.assertTrue(any(r['status']=='insufficient' for r in report['slices']))
    def test_fix(self):
        self.assertFalse(any(r['status']=='block' for r in evaluate('fixed')['slices']))

