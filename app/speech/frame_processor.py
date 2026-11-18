from typing import Protocol


class Processor(Protocol):
    def process(self, frame):
        ...


class FrameProcessor:

    def __init__(self):
        self.processors = []

    def add_processor(self, processor: Processor):
        self.processors.append(processor)

    def process(self, frame):

        for processor in self.processors:
            processor.process(frame)