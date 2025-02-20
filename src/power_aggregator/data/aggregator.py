import json
from pathlib import Path


class Aggregator(object):
    ON = 0
    OFF = 1

    def __init__(self, path: Path):
        with open(path) as fp:
            struct = json.load(fp)
            self.name = struct["name"]
            self.logo = Path(struct["logo"])
            self.sequence = struct["sequence"]
            if "transitions" in struct:
                trans = struct["transitions"]
                self.transitions = (trans["on"], trans["off"])
            else:
                self.transitions = None

    def __len__(self):
        if self.transitions:
            l = len(self.transitions[self.ON]) + len(self.transitions[self.OFF])
        else:
            l = 0
        return l + len(self.sequence)

    def __hash__(self):
        return hash(self.name)

    def fit(self, length: int) -> list[float]:
        output = []

        # Repeat pattern
        if len(self) >= length:
            offset = 0
            if self.transitions:
                output.extend(self.transitions[self.ON])
                offset = len(self.transitions[self.OFF])
            idx = 0
            while len(output) != length - offset:
                if idx >= len(self.sequence):
                    idx = 0
                output.append(self.sequence[idx])
                idx += 1
            if self.transitions:
                output.extend(self.transitions[self.OFF])

        # Cut pattern
        else:
            idx = 0
            while len(output) != length:
                if idx >= len(self.sequence):
                    idx = 0
                output.append(self.sequence[idx])
                idx += 1

        return output
