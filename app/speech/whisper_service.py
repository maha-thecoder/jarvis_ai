from transformers import pipeline

from core.logger import get_logger


logger=get_logger(__name__)


class WhisperService:


    def __init__(self):

        logger.info(
            "Loading Whisper"
        )


        self.pipe=pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-base",
            device="cpu"
        )


    def transcribe(self,path):


        result=self.pipe(
            path,
            generate_kwargs={
                "language":"english"
            }
        )


        return result["text"].strip()