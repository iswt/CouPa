import unittest
from lib.util import to_satoshis, from_satoshis

class TestUtil(unittest.TestCase):
	
	def test_to_satoshis(self):
		res1 = to_satoshis('1.4687')
		self.assertEqual(res1, 146870000)
		
	def test_from_satoshis(self):
		res1 = str(from_satoshis(146870000))
		self.assertEqual(res1, '1.46870000')
	
	