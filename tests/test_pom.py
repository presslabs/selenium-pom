# import os
from os import path

import pytest
from selenium.common.exceptions import TimeoutException

from selenium_pom.page import Element, Page


@pytest.fixture
def selenium(selenium):
    selenium.maximize_window()
    selenium._poll = 5
    return selenium


class BasicPageDiv(Element):
    textarea = Element(tag_name='textarea')
    span1 = Element(tag_name='span')
    span2 = Element(class_name='span2')


class BasicPage(Page):
    url = "file://" + path.join(path.dirname(__file__), 'pages/basic_page.html')
    div1 = BasicPageDiv(id='div1')
    div2 = BasicPageDiv(id='div2')


class DelayPage(BasicPage):
    url = "file://" + path.join(path.dirname(__file__), 'pages/delay_page.html')


def test_basic_page(selenium):
    basic_page = BasicPage(selenium)
    basic_page.goto()
    assert basic_page.div1.textarea.text == 'spam!'
    assert basic_page.div1.span2.text == 'span2 text'
    assert basic_page.div2.textarea.text == 'ham!'
    assert basic_page.div2.text == "span1 text span2 text ham!"


def test_dynamic_page(selenium):
    delay_page = DelayPage(selenium, timeout=0.1)
    delay_page.goto()
    # assert delay_page.div1.textarea.text == 'spam!'
    # assert delay_page.div1.span2.text == 'span2 text'
    with pytest.raises(TimeoutException) as excp:
        assert delay_page.div2.textarea.text == 'ham!'
    delay_page = DelayPage(selenium, timeout=2)
    selenium.execute_script('show_div2_delayed(100)');
    assert delay_page.div2.textarea.text == 'ham!'
    # assert delay_page.div2.text == "span1 text span2 text ham!"
