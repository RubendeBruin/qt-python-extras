"""
urlActionPage: A QWebEnginePage with callback for clicking links.
Intended to be used in conjunction with a webEngineView

example use:

.. code::python

    #Define a callback target
    def test(data):
        print(data)

    # create page and set callback
    page = urlActionPage()
    page.callback = test

    # generate an action url.
    action_data = 'hello world'
    action_url = page.create_action_url('hello world')
    
    # create some HTML
    html = '<html><a href="{}">link</a></html>'.format(action_url)
    page.setHtml(html)

    # and assign the page to a web-engine view
    ui.webEngineView.setPage(page)


"""

from PyQt5 import QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEnginePage


class urlActionPage(QtWebEngineWidgets.QWebEnginePage):

    def __init__(self):
        super().__init__()
        self.action_data = list()
        self.callback = None

    def acceptNavigationRequest(self, url: QtCore.QUrl, type: 'QWebEnginePage.NavigationType', isMainFrame: bool):
        """
        Overrides the default method
        Returns True if navigation is OK, returns False otherwise
        """
        text = url.path()

        if text.startswith('/action'):
            id = int(text[7:])
            if self.callback is None:
                raise Exception('callback not set - please set this.callback = your_function')

            try:
                data = self.action_data[id]
            except:
                raise Exception(
                    'data with id = {} is not available. Did you accidentally clear actions since creating the link?'.format(
                        id))
            self.callback(data)
            return False

        return True

    def create_action_url(self, link_data):
        self.action_data.append(link_data)
        i = len(self.action_data) - 1

        return 'http://action.now/action' + str(i) # the url needs to look like a real one

    def clear_actions(self):
        self.action_data.clear()




