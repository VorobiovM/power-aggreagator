from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from power_aggregator.components import ActionMenu, DraggableGraph, ScrollableButtons


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

        # Force first draw
        self.graph.changeBaselineFirst(self.menu.baselines[self.menu.combo_box.currentIndex()])
