import os
import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from power_aggregator.components import ActionMenu, DraggableGraph, ScrollableButtons

if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS  # Path of the PyInstaller temp directory
    favicon = Path(base_path, "favicon.png")
else:
    base_path = os.path.abspath(".")
    favicon = Path(base_path, "favicon.png")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Power Aggregator")

        self.menu = ActionMenu()
        self.graph = DraggableGraph()
        self.buttons = ScrollableButtons()

        self.menu.selectionChanged.connect(self.graph.changeBaseline)
        self.menu.button_clear.pressed.connect(self.graph.clearAggregators)
        self.menu.saveSignal.connect(self.graph.exportCsv)
        self.buttons.buttonClicked.connect(self.graph.changeAggregator)

        r_layout = QVBoxLayout()
        r_layout.addWidget(self.graph)
        r_layout.addWidget(self.menu)

        l_layout = QHBoxLayout()
        l_layout.addWidget(self.buttons)
        l_layout.addLayout(r_layout)

        container = QWidget()
        container.setLayout(l_layout)
        self.setCentralWidget(container)

        self.setWindowIcon(QIcon(favicon.as_posix()))

        # Force first draw
        self.graph.changeBaselineFirst(self.menu.baselines[self.menu.combo_box.currentIndex()])
