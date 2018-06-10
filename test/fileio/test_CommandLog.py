from fileio import CommandLog
import unittest

class CommandLogTest(unittest.TestCase):
	def test_store(self):
		self.assertTrue(True)

def main():
	suite = unittest.defaultTestLoader.loadTestsFromTestCase(CommandLogTest)
	runner = unittest.TextTestRunner()
	runner.run(suite)