class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value= value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		if self.props is None:
			return ""
    
		props_html = ""
		for key, value in self.props.items():
			props_html += f' {key}="{value}"'
		return props_html

	def __repr__(self):
		return self.HTMLNode

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value == None:
			raise ValueError
		if self.tag == None:
			return self.value

		leaf_props = self.props_to_html()
		return f"<{self.tag}{leaf_props}>{self.value}</{self.tag}>"

	def __repr__(self):
		return self.to_html


class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)
  
	def to_html(self):
		if self.tag == None:
			raise ValueError("Invalid HTML: no tag")
		if self.children == None:
			raise ValueError("Children value missing")

		children_props = self.props_to_html()
		children_combined = ""
		for child in self.children:
			children_combined += child.to_html()
		return f"<{self.tag}{children_props}>{children_combined}</{self.tag}>"