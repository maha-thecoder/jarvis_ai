from pathlib import Path
from datetime import datetime

import numpy as np
import soundfile as sf

from audio.frame import AudioFrame
from core.logger import get_logger


logger=get_logger(__name__)


class AudioRecorder:


    def __init__(self):

        self.output_dir=Path("recordings")

        self.output_dir.mkdir(exist_ok=True)

        self.frames=[]

        self.recording=False



    def start(self):

        self.frames.clear()

        self.recording=True

        logger.info("Recording started")



    def add_frame(self,frame:AudioFrame):

        if self.recording:

            self.frames.append(
                frame.data.copy()
            )



    def stop(self):

        if not self.recording:

            return None


        self.recording=False


        if not self.frames:

            return None



        audio=np.concatenate(
            self.frames,
            axis=0
        )


        audio=audio.squeeze()



        name=datetime.now().strftime(
            "speech_%Y%m%d_%H%M%S.wav"
        )


        path=self.output_dir/name



        sf.write(
            path,
            audio,
            16000,
            subtype="PCM_16"
        )


        logger.info(
            "Saved %s",
            path
        )


        return str(path)