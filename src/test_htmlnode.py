import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    """ def test_tohtml(self):
        node = HTMLNode("p", "test data 1")
        #print(f"test 1: {node}")
        try:
            node.to_html()
        except Exception as e:
            print(f"Error occurred: {e}")
        return
    
    def test_tohtml2(self):
        node = HTMLNode("p", "test data 1")
        node2 = HTMLNode("h1", "test data 2", [node])
        #print(f"test 2: {node2}")
        try:
            node2.to_html()
        except Exception as e:
            print(f"Error occurred: {e}")
        return """
    
    def test_propstohtml(self):
        node = HTMLNode("p", "test data 3", None, {"href": "https://www.google.com", "target": "_blank",})
        #node2 = HTMLNode()
        #print(f"test 3: {node}")
        text_props = node.props_to_html()
        #print(text_props)
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
    
    def test_leaf_to_html_novalue(self):
        try:
            node = LeafNode("a", None)
            print(node.to_html())
        except Exception as e:
            #print(f"Error occurred: {e}")
            return
        
    def test_leaf_to_html_valueonly(self):
        node = LeafNode(None, "this is just text")
        self.assertEqual(node.to_html(), "this is just text")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    




if __name__ == "__main__":
    unittest.main()