import json
import logging
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from core.logger import get_logger
from intent.models import IntentResult


logger = get_logger(__name__)


# Hide sentence-transformer progress logs
logging.getLogger(
    "sentence_transformers"
).setLevel(logging.ERROR)



class IntentRouter:


    def __init__(self):

        logger.info(
            "Loading Intent Model..."
        )


        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            cache_folder="models"
        )


        self.confidence_threshold = 0.55


        self.intents = self.load_intents()


        self.embeddings = {}


        self.prepare_embeddings()


        logger.info(
            "Intent Router Ready"
        )



    # --------------------------------
    # Load intent database
    # --------------------------------

    def load_intents(self):


        file_path = (
            Path(__file__).parent
            / "intent.json"
        )


        if not file_path.exists():

            raise FileNotFoundError(
                f"Intent file missing: {file_path}"
            )


        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)



    # --------------------------------
    # Create embeddings
    # --------------------------------

    def prepare_embeddings(self):


        for item in self.intents:


            intent_name = item["intent"]

            examples = item["examples"]


            self.embeddings[intent_name] = (
                self.model.encode(
                    examples,
                    convert_to_tensor=True
                )
            )


            logger.info(
                "Loaded intent: %s",
                intent_name
            )



    # --------------------------------
    # Classify user text
    # --------------------------------

    def classify(
        self,
        text: str
    ) -> IntentResult:


        query_embedding = (
            self.model.encode(
                text,
                convert_to_tensor=True
            )
        )


        best_intent = "UNKNOWN"

        best_score = 0.0



        for intent, embedding in self.embeddings.items():


            similarity = cos_sim(
                query_embedding,
                embedding
            )


            score = float(
                max(similarity[0])
            )


            if score > best_score:

                best_score = score

                best_intent = intent



        # Reject weak matches

        if best_score < self.confidence_threshold:

            best_intent = "UNKNOWN"



        logger.info(
            "Intent=%s Confidence=%.2f",
            best_intent,
            best_score
        )



        return IntentResult(

            name=best_intent,

            confidence=best_score,

            text=text

        )