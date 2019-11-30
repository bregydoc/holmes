from dataclasses import dataclass
import time
from typing import List


@dataclass
class RawEntry:
    title: str
    url: str
    raw_body: str
    principal_image_url: str = ""
    sentiment: float = 0.5
    timestamp: float = time.time()


@dataclass
class SourceDescription:
    name: str
    version: str = "0.0.1"


class RawSource:
    def __init__(self):
        self.dataset: List[RawEntry] = []

    def add_new_raw_entry(self, entry: RawEntry):
        self.dataset.append(entry)

    def describe(self) -> SourceDescription:
        pass

    def load_info_person(self, person_name: str):
        pass
