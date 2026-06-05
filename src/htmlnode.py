class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value= value
		self.children = children
		self.props = props

	def toHTML(self):
		raise NotImplementedError

	def props_to_html(self):
		if self.props == None or self.props == "":
			return ""
		return f" href={self.props.href} target={self.props.target}"

	def __repr__(self):
		print (self.HTMLNode.values)
