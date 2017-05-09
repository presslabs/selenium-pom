from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import logging


LOCATORS = {
    'class_name': By.CLASS_NAME,
    'css_selector': By.CSS_SELECTOR,
    'id': By.ID,
    'link_text': By.LINK_TEXT,
    'name': By.NAME,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag_name': By.TAG_NAME,
    'xpath': By.XPATH,
}


def get_locator(kwargs):
    assert len(kwargs) == 1
    by, expression = list(kwargs.items())[0]
    return (LOCATORS[by], expression)


class Element(object):
    def __init__(self, parent=None, timeout=None, **kwargs):
        self.parent = parent
        if len(kwargs) == 0 and parent is None:
            self._locator = None  # will be copied from the prototype, see new
        else:
            self._locator = get_locator(kwargs)

    def __get__(self, obj, objtype):
        return self.new(parent=obj)

    def new(self, parent):
        assert self.parent is None
        new_element = type(self)()
        new_element.__dict__ = self.__dict__.copy()
        new_element.parent = parent
        return new_element

    @property
    def timeout(self):
        return self.parent.timeout

    def wait_visible(self):
        """Wait for the element to be visible"""
        el =  WebDriverWait(self.parent, self.timeout).until(
            EC.presence_of_element_located(self._locator))
        el = WebDriverWait(self.parent, self.parent.timeout).until(
            EC.visibility_of(el)
        )
        return el

    def wait_clickable(self):
        """Wait for the element to be clickable"""
        return WebDriverWait(self.parent, self.parent.timeout).until(
            EC.element_to_be_clickable(self._locator)
        )

    def click(self):
        el = self.wait_clickable()
        el.click()

    def clear(self):
        el = self.wait_clickable()
        el.clear()

    def send_keys(self, keys):
        el = self.wait_clickable()
        el.send_keys(keys)

    @property
    def text(self):
        el = self.wait_visible()
        return el.text

    def hover(self):
        el = self.wait_visible()
        ActionChains(self.parent).move_to_element(el).perform()

    def __getattr__(self, attr_name):
        if self.parent is None:
            raise AttributeError(attr_name)
        return getattr(self.parent.find_element(*self._locator), attr_name)


class Page(object):
    def __init__(self, driver, timeout=2):
        self.parent = driver
        self.timeout = timeout

    def goto(self, url_extra=""):
        self.parent.get(self.url + url_extra)

    def __getattr__(self, attr_name):
        # print attr_name
        return getattr(self.parent, attr_name)
