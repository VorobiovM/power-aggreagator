import json
import math
from itertools import repeat
from pathlib import Path

DAY_IN_MIN = 24 * 60


class Baseline(object):
    def __init__(self, path: Path):
        with open(path) as fp:
            struct = json.load(fp)
            self.name = struct["name"]
            sequence = struct["sequence"]
            sequence = repeat(sequence, math.ceil(DAY_IN_MIN / len(struct["sequence"])))
            sequence = list(sequence)
            self.sequence = []
            for s in sequence:
                self.sequence.extend(s)
            self.sequence = self.sequence[:DAY_IN_MIN]
