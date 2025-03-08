
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html not implemented at this level")
    
    def props_to_html(self):
        html_content = ""
        for attribute_type, content in self.props.items():
            html_content = html_content + " " + attribute_type + "=\"" + content + "\""
        return html_content
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            #debug
            print(self)
            raise ValueError("value cannot be blank for a leaf node")
        if self.tag == None:
            return self.value
        if self.props == None:
            constructed_html = f"<{self.tag}>{self.value}</{self.tag}>"
            return constructed_html
        constructed_html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return constructed_html
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("tag cannot be blank for ParentNode")
        if self.children == None:
            raise ValueError("children cannot be blank for ParentNode")
        constructed_html = f"<{self.tag}"
        if self.props != None:
            constructed_html = constructed_html + f"{self.props_to_html()}"
        constructed_html = constructed_html + ">"
        for child in self.children:
            constructed_html = constructed_html + child.to_html()
        constructed_html = constructed_html + f"</{self.tag}>"
        return constructed_html
        
        



    
