import unittest
from blocks import *

class TestMarkdowntoBlocks(unittest.TestCase):

    def test_markdown_plain(self):
        md = "plain string"
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks, ["plain string",])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items




"""
        blocks = markdown_to_blocks(md)
        #print(f"BLOCKS: {blocks}")
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_code_block(self):
        # Valid code block
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        # Invalid code block (missing closing backticks)
        block = "```\ncode line 1\ncode line 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block(self):
        # Valid quote block
        block = "> This is a quote\n> This is another line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        # Invalid quote block (one line doesn't start with >)
        block = "> This is a quote\nThis is not a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        # Valid unordered list
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        # Invalid unordered list (missing space after -)
        block = "-Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        # Valid ordered list
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        # Invalid ordered list (numbers not sequential)
        block = "1. Item 1\n3. Item 2\n2. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Invalid ordered list (missing space after .)
        block = "1.Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        # Normal paragraph
        block = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Mixed content that doesn't match any block type
        block = "> This is not a quote\n- This is not a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
class TestMarkdowntoHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

        def test_headings(self):
            md = """
# Heading 1
## Heading 2
### Heading 3
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
            )

    def test_quote(self):
        md = """
> This is a quote
> This is another line
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nThis is another line</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. Item 1
2. Item 2
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )

    def test_edge_cases(self):
        # 1. Empty Markdown Input
        md = ""
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div></div>")

        # 2. Markdown with Only Whitespace
        md = "   \n\t\n   "
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div></div>")

        # 3. Code Block with Empty Content
        md = "``````"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><pre><code></code></pre></div>")

        # 4. Code Block with Only Newlines
        md = "```\n\n```"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><pre><code></code></pre></div>")

        # 5. Heading with No Text
        md = "#"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h1></h1></div>")

        # 6. Quote Block with Empty Lines
        md = ">\n>\n>"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><blockquote>\n\n</blockquote></div>")

        # 7. Unordered List with Empty Items
        md = "- \n- "
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><ul><li></li><li></li></ul></div>")

        # 8. Ordered List with Non-Sequential Numbers
        md = "2. Item 1\n3. Item 2"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><p>2. Item 1 3. Item 2</p></div>")

    def test_extract_title(self):
        # Test case 1: Valid H1 header
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

        # Test case 2: H1 header with leading/trailing whitespace
        markdown = "#   Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

        # Test case 3: No H1 header
        markdown = "## Subheading\nThis is a paragraph."
        try:
            extract_title(markdown)
        except ValueError as e:
            self.assertEqual(str(e), "No H1 header found in the markdown content.")

        # Test case 4: Multiple headers, first one is H1
        markdown = """
# Title
## Subheading
### Sub-subheading
"""
        self.assertEqual(extract_title(markdown), "Title")

        # Test case 5: H1 header not at the start
        markdown = """
Some text
# Title
More text
"""
        self.assertEqual(extract_title(markdown), "Title")





if __name__ == "__main__":
    unittest.main()