import webbrowser

from core.logger import get_logger


logger = get_logger(__name__)


class BrowserTool:


    def search(self, query):

        logger.info(
            "Searching web: %s",
            query
        )


        url = (
            "https://www.google.com/search?q="
            + query.replace(" ","+")
        )


        webbrowser.open(url)