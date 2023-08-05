import mistune


class ConfluenceTag(object):
    def __init__(self, name, text='', attrib=None, namespace='ac', cdata=False):
        self.name = name
        self.text = text
        self.namespace = namespace
        if attrib is None:
            attrib = {}
        self.attrib = attrib
        self.children = []
        self.cdata = cdata

    def render(self):
        namespaced_name = self.add_namespace(self.name, namespace=self.namespace)
        namespaced_attribs = {
            self.add_namespace(attribute_name, namespace=self.namespace): attribute_value
            for attribute_name, attribute_value in self.attrib.items()
        }

        content = '<{}{}>{}{}</{}>'.format(
            namespaced_name,
            ' {}'.format(' '.join(['{}="{}"'.format(name, value) for name, value in sorted(namespaced_attribs.items())])) if namespaced_attribs else '',
            ''.join([child.render() for child in self.children]),
            '<![CDATA[{}]]>'.format(self.text) if self.cdata else self.text,
            namespaced_name
        )
        return '{}\n'.format(content)

    @staticmethod
    def add_namespace(tag, namespace):
        return '{}:{}'.format(namespace, tag)

    def append(self, child):
        self.children.append(child)


class ConfluenceRenderer(mistune.Renderer):
    def structured_macro(self, name):
        return ConfluenceTag('structured-macro', attrib={'name': name})

    def parameter(self, name, value):
        parameter_tag = ConfluenceTag('parameter', attrib={'name': name})
        parameter_tag.text = value
        return parameter_tag

    def plain_text_body(self, text):
        body_tag = ConfluenceTag('plain-text-body', cdata=True)
        body_tag.text = text
        return body_tag

    def block_code(self, code, lang=None):
        root_element = self.structured_macro('code')
        if lang is not None:
            lang_parameter = self.parameter(name='language', value=lang)
            root_element.append(lang_parameter)
        root_element.append(self.parameter(name='linenumbers', value='true'))
        root_element.append(self.plain_text_body(code))
        return root_element.render()

    def image(self, src, title, text):
        attributes = {'alt': text}
        if title:
            attributes['title'] = title

        root_element = ConfluenceTag(name='image', attrib=attributes)
        url_tag = ConfluenceTag('url', attrib={'value': src}, namespace='ri')
        root_element.append(url_tag)

        return root_element.render()
