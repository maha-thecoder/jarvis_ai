import re

from core.logger import get_logger


logger = get_logger(__name__)


class EntityExtractor:


    def extract_app_name(
        self,
        text: str
    ) -> str:


        text = text.lower()


        apps = {

            "chrome":
            [
                "chrome",
                "google chrome",
                "browser"
            ],


            "vscode":
            [
                "vs code",
                "visual studio",
                "code editor"
            ],


            "notepad":
            [
                "notepad",
                "text editor"
            ],

        }



        for app, keywords in apps.items():

            for keyword in keywords:

                if keyword in text:

                    logger.info(
                        "App entity detected: %s",
                        app
                    )

                    return app



        return ""
