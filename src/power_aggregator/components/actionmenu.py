import os
from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget

from power_aggregator.data import Baseline


ROOT = Path(__file__).parents[1]


class ActionMenu(QWidget):
    selectionChanged = pyqtSignal(Baseline)
    saveSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.combo_box = QComboBox()
        self.baselines = []
        self.readBaselines()
        self.baselines.sort(key=lambda x: x.name)
        names = [b.name for b in self.baselines]
        self.combo_box.addItems(names)
        self.combo_box.setCurrentIndex(len(names) - 1)

        self.button_clear = QPushButton("Clear")
        self.button_export = QPushButton("Export")
        self.line_export = QLineEdit("output.csv")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.line_export)
        button_layout.addWidget(self.button_clear)
        button_layout.addWidget(self.button_export)

        layout.addWidget(self.combo_box)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.combo_box.currentIndexChanged.connect(self.emit_selection)
        self.button_export.pressed.connect(self.emit_save)

    def readBaselines(self):
        path = Path(ROOT, "data/baselines")
        for _, _, files in os.walk(path):
            for file in files:
                self.baselines.append(Baseline(Path(path, file)))

    def emit_selection(self, idx):
        self.selectionChanged.emit(self.baselines[idx])

    def emit_save(self):
        self.saveSignal.emit(self.line_export.text())
