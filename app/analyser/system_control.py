import datetime

from core.logger import get_logger


logger = get_logger(__name__)


class SystemControl:


    def get_time(self):

        now = datetime.datetime.now()

        result = now.strftime(
            "%I:%M %p"
        )


        logger.info(
            "Current time %s",
            result
        )


        print(
            f"The time is {result}"
        )