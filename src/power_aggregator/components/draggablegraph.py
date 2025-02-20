import os
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd
from PyQt6.QtCharts import QChart, QChartView, QLineSeries
from PyQt6.QtCore import QPointF, QRectF, Qt, pyqtSlot
from PyQt6.QtGui import QBrush, QPainter, QPen

from power_aggregator.data import Aggregator, Baseline

if getattr(sys, "frozen", False):
    base_path = sys.executable  # Path of the PyInstaller executable
    base_path = Path(base_path).parent
else:
    base_path = os.path.abspath(".")


class DraggableGraph(QChartView):
    def __init__(self):
        super().__init__()
        self.chart = QChart()
        self.setChart(self.chart)
        self.series = QLineSeries()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.selected_range = None
        self.selection_rect = None
        self.baseline = None
        self.aggregator = None
        self.aggregators = defaultdict(list)

    def draw(self):
        self.series.clear()
        self.addBaseline()
        self.addAggregators()
        self._adjustScale()

    def partialDraw(self, aggregator, start, stop):
        self._calcAggregator(aggregator, start, stop)
        self._adjustScale()

    def coldDraw(self):
        self.addBaseline()
        self._adjustScale()
        self.chart.axes(Qt.Orientation.Horizontal)[0].setRange(0, len(self.baseline.sequence))

    def addBaseline(self):
        for i, s in enumerate(self.baseline.sequence):
            self.series.append(i, s)

    def addAggregators(self):
        for aggregator, ranges in self.aggregators.items():
            for start, stop in ranges:
                self._calcAggregator(aggregator, start, stop)

    def _adjustScale(self):
        points = [p.y() for p in self.series.points()]
        max_y = max(points)
        self.chart.axes(Qt.Orientation.Vertical)[0].setRange(0, (max_y + 100) * 1.2)

    def _calcAggregator(self, agg, start, stop):
        p = agg.fit(stop - start)
        for idx in range(start, stop):
            old = self.series.at(idx)
            new = QPointF(old.x(), old.y() + p[idx - start])
            self.series.replace(old, new)

    @pyqtSlot()
    def clearAggregators(self):
        self.aggregators.clear()
        self.draw()

    @pyqtSlot(str)
    def exportCsv(self, path: str):
        if not path.endswith(".csv"):
            path += ".csv"
        path = Path(base_path, path)
        points = [p.y() for p in self.series.points()]
        df = pd.DataFrame(points, columns=["power"])
        df.to_csv(path)

    @pyqtSlot(Baseline)
    def changeBaselineFirst(self, baseline: Baseline):
        self.baseline = baseline
        self.coldDraw()

    @pyqtSlot(Baseline)
    def changeBaseline(self, baseline: Baseline):
        self.baseline = baseline
        self.draw()

    @pyqtSlot(Aggregator)
    def changeAggregator(self, aggregator: Aggregator):
        self.aggregator = aggregator

    def mousePressEvent(self, event):
        if self.aggregator and event.button() == Qt.MouseButton.LeftButton:
            self.selected_range = event.pos().x()
            self.selection_rect = QRectF(self.selected_range, 0, 0, self.height())
            self.viewport().update()

    def mouseMoveEvent(self, event):
        if self.selected_range is not None:
            start_x = min(self.selected_range, event.pos().x())
            width = abs(event.pos().x() - self.selected_range)
            self.selection_rect = QRectF(start_x, 0, width, self.height())
            self.viewport().update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.selected_range is not None:
            release = event.pos().x()
            mi, ma = min(self.selected_range, release), max(self.selected_range, release)

            # Convert pixel to chart coordinates
            mi = self.chart.mapToValue(QPointF(mi, 0), self.series).x()
            ma = self.chart.mapToValue(QPointF(ma, 0), self.series).x()

            # Find closest indices
            indices = [point.x() for point in self.series.points()]
            mi = int(min(indices, key=lambda x: abs(x - mi)))
            ma = int(min(indices, key=lambda x: abs(x - ma)))

            self.aggregators[self.aggregator].append((mi, ma))
            self.selected_range = None
            self.selection_rect = None
            self.viewport().update()
            self.partialDraw(self.aggregator, mi, ma)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.selection_rect:
            painter = QPainter(self.viewport())
            painter.setBrush(QBrush(Qt.GlobalColor.blue, Qt.BrushStyle.Dense4Pattern))
            painter.setPen(QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.DashLine))
            painter.drawRect(self.selection_rect)
