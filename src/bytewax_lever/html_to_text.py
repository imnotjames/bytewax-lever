from io import StringIO
from html.parser import HTMLParser


class TextFromHTMLGenerator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, data):
        self.text.write(data)

    def get_text(self):
        return self.text.getvalue()


def html_to_text(html: str):
    s = TextFromHTMLGenerator()
    s.feed(html)
    return s.get_text()
