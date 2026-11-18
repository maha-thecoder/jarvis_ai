from pathlib import Path
from datetime import datetime
import json


class SessionManager:


    def __init__(self):

        self.transcripts=[]

        self.summary_dir=Path(
            "memory/summaries"
        )

        self.summary_dir.mkdir(
            parents=True,
            exist_ok=True
        )


    def add_text(self,text):

        self.transcripts.append(
            {
                "time":
                str(datetime.now()),

                "text":text
            }
        )


    def save_session(self):

        if not self.transcripts:
            return


        filename=(
            datetime.now()
            .strftime(
            "session_%Y%m%d_%H%M%S.json"
            )
        )


        path=self.summary_dir/filename


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.transcripts,
                f,
                indent=4
            )


        print(
            "Session saved:",
            path
        )


    def cleanup_recordings(self):

        folder=Path(
            "recordings"
        )


        if not folder.exists():
            return


        for file in folder.glob("*.wav"):

            file.unlink()


        print(
            "Recordings cleaned"
        )