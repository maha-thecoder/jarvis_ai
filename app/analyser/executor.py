from core.logger import get_logger

from analyser.app_launcher import AppLauncher
from analyser.browser import BrowserTool
from analyser.system_control import SystemControl
from analyser.entity_extractor import EntityExtractor



logger = get_logger(__name__)


class ToolExecutor:


    def __init__(self):

        self.app_launcher = AppLauncher()

        self.browser = BrowserTool()

        self.system = SystemControl()

        self.extractor = EntityExtractor()



    def execute(
        self,
        intent
    ):


        logger.info(
            "Executing %s",
            intent.name
        )



        if intent.name == "OPEN_APP":


            app = self.extractor.extract_app_name(
                intent.text
            )


            if app:

                self.app_launcher.open(
                    app
                )

            else:

                logger.warning(
                    "Application not identified"
                )



        elif intent.name == "SEARCH_WEB":


            self.browser.search(
                intent.text
            )



        elif intent.name == "GET_TIME":


            self.system.get_time()



        else:


            logger.warning(
                "No analyser available"
            )