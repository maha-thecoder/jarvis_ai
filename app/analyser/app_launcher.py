import subprocess
import platform

from core.logger import get_logger


logger = get_logger(__name__)


class AppLauncher:


    def open(self, app_name: str):

        app_name = app_name.lower()


        logger.info(
            "Opening application: %s",
            app_name
        )


        system = platform.system()


        try:

            if "chrome" in app_name:

                if system == "Windows":

                    subprocess.Popen(
                        "start chrome",
                        shell=True
                    )


            elif "vscode" in app_name or "visual studio" in app_name:

                subprocess.Popen(
                    "code",
                    shell=True
                )


            elif "notepad" in app_name:

                subprocess.Popen(
                    "notepad"
                )


            else:

                logger.warning(
                    "Unknown application %s",
                    app_name
                )


        except Exception:

            logger.exception(
                "Failed opening application"
            )