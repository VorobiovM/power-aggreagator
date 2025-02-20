import os
from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QPushButton, QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from power_aggregator.data import Aggregator


ROOT = Path(__file__).parents[1]


class ScrollableButtons(QWidget):
    buttonClicked = pyqtSignal(Aggregator)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        button_container = QWidget()
        button_layout = QVBoxLayout()
        self.aggregators = []
        self.buttons = []

        path = Path(ROOT, "data/aggregators")
        for _, _, files in os.walk(path):
            for file in files:
                aggregator = Aggregator(Path(path, file))
                self.aggregators.append(aggregator)
                btn = QPushButton()
                btn.setCheckable(True)
                btn.setBaseSize(80, 80)
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                image = QPixmap(Path(ROOT, aggregator.logo).as_posix())
                icon = QIcon(image)
                btn.setIcon(icon)
                btn.setIconSize(btn.size() * 0.1)
                btn.clicked.connect(self.on_button_clicked)
                self.buttons.append(btn)
                button_layout.addWidget(btn)

        button_layout.addSpacerItem(QSpacerItem(80, 0, vPolicy=QSizePolicy.Policy.MinimumExpanding))
        button_container.setLayout(button_layout)
        scroll_area.setWidget(button_container)
        layout.addWidget(scroll_area)
        self.setLayout(layout)
        self.setFixedWidth(140)

    def on_button_clicked(self):
        for idx, btn in enumerate(self.buttons):
            if btn != self.sender():
                btn.setChecked(False)
                continue

            self.buttonClicked.emit(self.aggregators[idx])
