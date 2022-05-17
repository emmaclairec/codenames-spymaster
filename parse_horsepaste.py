import sys
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import warnings
warnings.filterwarnings("ignore", message="_CFURLCopyResourcePropertyValuesAndFlags failed "
                                          "because it was passed an URL which has no scheme")

def parse(url):

    def render(source_url):
        """Fully render HTML, JavaScript and all."""

        class Render(QWebEngineView):
            def __init__(self, url):
                self.html = None
                self.app = QApplication(sys.argv)
                QWebEngineView.__init__(self)
                self.loadFinished.connect(self._loadFinished)
                # self.setHtml(html)
                self.load(QUrl(url))
                self.app.exec_()

            def _loadFinished(self, result):
                # This is an async call, you need to wait for this
                # to be called before closing the app
                self.page().toHtml(self._callable)

            def _callable(self, data):
                self.html = data
                # Data has been stored, it's safe to quit the app
                self.app.quit()

        return Render(source_url).html

    all_html = render(url)
    soup = BeautifulSoup(all_html, "html.parser")

    blue_hidden_tags = soup.findAll('div', {"class": "cell blue hidden-word"})
    blue = [tag.span.text for tag in blue_hidden_tags]
    red_hidden_tags = soup.findAll('div', {"class": "cell red hidden-word"})
    red = [tag.span.text for tag in red_hidden_tags]
    neutral_hidden_tags = soup.findAll('div', {"class": "cell neutral hidden-word"})
    neutral = [tag.span.text for tag in neutral_hidden_tags]
    black_hidden_tags = soup.findAll('div', {"class": "cell black hidden-word"})
    black = [tag.span.text for tag in black_hidden_tags]

    return [blue, red, neutral, black]
