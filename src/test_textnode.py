import unittest

from textnode import *
from htmlnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = TextNode("bold am i", TextType.BOLD)
        node2 = TextNode("bold am i", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("test me right now", TextType.TEXT)
        node2 = TextNode("test me right now", TextType.TEXT)
        self.assertEqual(node, node2)
    
    def test_uneq2(self):
        node = TextNode("test me right now", TextType.TEXT, "HTTPS://google.com")
        node2 = TextNode("test me right now", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("this is a bold node", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "this is a bold node")

    def test_italic(self):
        node = TextNode("this is an italic node", TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "this is an italic node")
    
    def test_code(self):
        node = TextNode ("this is a code node", TextType.CODE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "this is a code node")
    
    def test_link(self):
        node = TextNode(None, TextType.LINK, "https://www.mysite.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.mysite.com"})

    def test_image(self):
        node = TextNode("this is a bear", TextType.IMAGE, "https://www.mysite.com/bear.jpg")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://www.mysite.com/bear.jpg", "alt": "this is a bear"})



if __name__ == "__main__":
    unittest.main()