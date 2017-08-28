from __future__ import print_function

import importlib
import os

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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


class LazyElement(object):
    """Use this to for recursive structures

    Usage examples:

    replies = LazyElement('tests.pages.front.Comments', css_selector='ol')
    # the class is in the same module you can just reference it by name
    replies = LazyElement('Comments', css_selector='ol')
    """

    def __init__(self, klass_name, **kwargs):
        self._kwargs = kwargs
        self.klass_locator = klass_name

    def __get__(self, obj, objtype):
        if '.' in self.klass_locator:
            module_name, klass_name = self.klass_locator.rsplit('.', 1)
        else:
            module_name = objtype.__module__
            klass_name = self.klass_locator
        module = importlib.import_module(module_name)
        klass = getattr(module, klass_name)
        return klass(**self._kwargs).new(parent=obj)


class Element(object):
    def __init__(self, parent=None, **kwargs):
        self.parent = parent
        if len(kwargs) == 0 and parent is None:
            self._locator = None  # will be copied from the prototype, see new
        else:
            self._locator = get_locator(kwargs)
        if parent is not None:
            self.wait_visible()

    def _repr_locator(self):
        return self.parent._repr_locator() + " / {!r}:{!r}".format(
            *self._locator)

    def __repr__(self):
        return "<{} {}>".format(type(self).__name__, self._repr_locator())

    def __get__(self, obj, _):
        return self.new(parent=obj)

    def new(self, parent):
        assert self.parent is None
        new_element = type(self)()
        new_element.__dict__ = self.__dict__.copy()
        new_element.parent = parent
        return new_element

    @property
    def driver(self):
        return self.parent.driver

    @property
    def element(self):
        return self.parent.find_element(*self._locator)

    @property
    def timeout(self):
        return self.parent.timeout

    def is_visible(self):
        return self.is_present() and self.element.is_displayed()

    def is_present(self):
        try:
            _ = self.element
        except NoSuchElementException:
            return False
        return True

    def wait_visible(self, timeout=None):
        """Wait for the element to be visible"""
        if timeout is None:
            timeout = self.timeout

        if isinstance(self.parent, Element):
            parent_el = self.parent.element
        else:
            parent_el = self.parent

        return WebDriverWait(parent_el, timeout).until(
            EC.visibility_of_element_located(self._locator))

    def wait_clickable(self, timeout=None):
        """Wait for the element to be clickable"""
        if timeout is None:
            timeout = self.timeout
        return WebDriverWait(self.driver, timeout).until(
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

    def input(self, keys):
        self.clear()
        self.send_keys(keys)

    @property
    def text(self):
        el = self.wait_visible()
        return el.text

    def hover(self):
        el = self.wait_visible()
        ActionChains(self.driver).move_to_element(el).perform()

    @property
    def w3c(self):
        return self.parent.w3c

    def __getattr__(self, attr_name):
        if self.parent is None:
            raise AttributeError(attr_name)
        return getattr(self.element, attr_name)


class Page(object):
    def __init__(self, driver, timeout=None):
        if timeout is None:
            timeout = int(os.getenv('SELENIUM_TIMEOUT', '20'))
        self.parent = driver
        self.timeout = timeout

    def _repr_locator(self):
        return ""

    @property
    def driver(self):
        return self.parent

    def goto(self, url_extra=""):
        self.parent.get(self.url + url_extra)

    def __getattr__(self, attr_name):
        return getattr(self.parent, attr_name)

    def _recursive_attr_get(self, attr_name):
        attributes = attr_name.split('.')
        obj = self
        for attr in attributes:
            obj = getattr(obj, attr)
        return obj

    def reload_until(self, attr_name, verifier=lambda page, el: True):
        try_count = 0
        timeout = self.timeout / 5.0
        while True:
            try:
                el = self._recursive_attr_get(attr_name)
                el.wait_visible(timeout=timeout)
                assert verifier(self, el)
            except:
                if try_count >= 10:
                    raise

            if try_count >= 10:
                assert False

            try_count += 1
            self.goto()
