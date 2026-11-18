from core.logger import get_logger

logger = get_logger(__name__)


class WakeWordDetector:

    def __init__(self):

        self.wake_words = [
            "jarvis",
            "hey jarvis",
            "ok jarvis",
            "okay jarvis",
        ]


    def detect(self,text:str)->bool:

        text=text.lower().strip()


        # remove punctuation
        text=text.replace(",","")
        text=text.replace(".","")


        for word in self.wake_words:

            if word in text:

                logger.info(
                    "Wake Word Detected"
                )

                return True


        return False