import unittest
from lib.mnemonic import CounterpartyMnemonic

class TestCounterpartyMnemonic(unittest.TestCase):
	
	def test_from_phrase_xprv(self):
		c = CounterpartyMnemonic()
		k = c.from_phrase('heaven heaven heaven heaven heaven heaven heaven heaven heaven heaven heaven heaven')
		xprv = k.ExtendedKey(private=True)
		expected = 'xprv9s21ZrQH143K2FcPwU2qbiyqsNw3fG81rhj4Rf3vK7BTMwmSzhyZpDgpp7qHKYX58YjZTTEiMmeH1k9F2ejsAt6H5jEZCSZHtZSfactvNS9'
		self.assertEqual(expected, xprv)
		
	def test_from_phrase_xpub(self):
		c = CounterpartyMnemonic()
		k = c.from_phrase('heaven heaven heaven heaven heaven heaven heaven heaven heaven heaven heaven heaven')
		xpub = k.ExtendedKey(private=False)
		expected = 'xpub661MyMwAqRbcEjgs3VZqxrvaRQmY4iqsDvefE3TXsSiSEk6bYFHpN21JfQUYVSDum4jAWeZfg2ZhEKDZoBRmGcMdq5ZzbjB7PkdVKbVroyM'
		self.assertEqual(expected, xpub)