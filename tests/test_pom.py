# import os
from os import path

import pytest

from selenium_pom.page import Element, Page


@pytest.fixture
def selenium(selenium):
    selenium.maximize_window()
    return selenium


class BasicPageDiv(Element):
    def __init__(self, *a, **kwa):
        super(BasicPageDiv, self).__init__(*a, **kwa)
        self.textarea = Element(self, tag_name='textarea')
        self.span1 = Element(self, tag_name='span')
        self.span2 = Element(self, class_name='span2')


class BasicPage(Page):
    url = "file://" + path.join(path.dirname(__file__), 'pages/basic_page.html')
    def __init__(self, *a, **kwa):
        super(BasicPage, self).__init__(*a, **kwa)
        self.div1 = BasicPageDiv(self, id='div1')
        self.div2 = BasicPageDiv(self, id='div2')


@pytest.fixture
def basic_page(selenium):
    return BasicPage(selenium)


def test_pom(basic_page):
    basic_page.goto()
    assert basic_page.div1.textarea.text == 'spam!'
    assert basic_page.div1.span2.text == 'span2 text'
    assert basic_page.div2.textarea.text == 'ham!'
    assert basic_page.div2.text == "span1 text span2 text ham!"
