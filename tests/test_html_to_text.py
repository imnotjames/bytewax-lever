from bytewax_lever.html_to_text import html_to_text


def test_converts_html_entities():
    actual = html_to_text("Example &amp; Hello World")
    assert actual == "Example & Hello World"


def test_removes_html_entities_retaining_text():
    actual = html_to_text("<li>Hello <b>World</b></li>")
    assert actual == "Hello World"


def test_removes_html_with_attributes():
    actual = html_to_text('<li class="foo">Hello <b>World</b></li>')
    assert actual == "Hello World"


def test_removes_custom_elements():
    actual = html_to_text("<example>Hello <b>World</b></example>")
    assert actual == "Hello World"


def test_removes_invalid_html():
    actual = html_to_text("<li>Hello World")
    assert actual == "Hello World"


def test_retains_newlines():
    actual = html_to_text("<li>Hello World</li>\n<li>Hello Mars</li>")
    assert actual == "Hello World\nHello Mars"
