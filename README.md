Page Object Model for Selenium
==============================

THIS IS WORK IN PROGRESS! EXPECT CONSTANT API CHANGES!

This library provides a basic page object mode for selenium.

Quick example
-------------

    # define a complex element that nests other elements
    class BasicPageDiv(Element):
        textarea = Element(tag_name='textarea')
        span1 = Element(tag_name='span')
        span2 = Element(class_name='span2')
    
    # define the page
    class BasicPage(Page):
        url = "file://" + path.join(path.dirname(__file__), 'pages/basic_page.html')
        div1 = BasicPageDiv(id='div1')

    # example usage
    def test_basic_page(selenium):
        basic_page = BasicPage(selenium)
        basic_page.goto()
        assert basic_page.div1.textarea.text == 'spam!'
        assert basic_page.div1.span2.text == 'span2 text'
    
