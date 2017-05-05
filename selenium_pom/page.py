from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


LOCATORS = {
    'id': By.ID,
    'xpath': By.XPATH,
    'tag_name': By.TAG_NAME,
    'class_name': By.CLASS_NAME,
}


def get_locator(kwargs):
    assert len(kwargs) == 1
    by, expression = list(kwargs.items())[0]
    return (LOCATORS[by], expression)


class Element(object):
    def __init__(self, page, timeout=None, **kwargs):
        self.driver = page
        self._locator = get_locator(kwargs)
        self.timeout = page.timeout if timeout is None else timeout

    def wait_visible(self):
        """Wait for the element to be visible"""
        pass

    def wait_clickable(self):
        """Wait for the element to be clickable"""
        return WebDriverWait(self.driver, self.timeout).until(
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

    def __getattr__(self, attr_name):
        return getattr(self.driver.find_element(*self._locator), attr_name)


class Page(object):
    def __init__(self, driver, timeout=2):
        self.driver = driver
        self.timeout = timeout

    def goto(self):
        self.driver.get(self.url)

    def __getattr__(self, attr_name):
        # print attr_name
        return getattr(self.driver, attr_name)
