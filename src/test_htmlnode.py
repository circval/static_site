import unittest
from htmlnode import HTMLNode

class HTMLTestNode(unittest.TestCase):
	def test_1(self):
		HTMLNode("p", "google it", "pp", {"href": "https://www.google.com"})

	def test_2(self):
		HTMLNode(6, "google it", "8", {"href": "https://www.google.com"})

	def test_3(self):
		HTMLNode("test", 5, "5", {"href": "https://www.google.com"})
if __name__ == "__main__":
        unittest.main()
