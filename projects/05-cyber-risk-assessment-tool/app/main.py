from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QSplitter,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from models import RiskItem
from scoring import (
    calculate_inherent_score,
    calculate_residual_score,
    classify_risk,
    matrix_counts,
    summarize_risks,
)
from storage import export_csv, load_risks, load_scenario, save_risks

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "risk_register.json"
SCENARIO_PATH = PROJECT_ROOT / "data" / "ransomware_scenario.json"

CATEGORIES = [
    "Operational",
    "Ransomware",
    "Identity",
    "Third-Party",
    "Data Protection",
    "Governance",
]

STATUSES = ["Open", "Mitigating", "Accepted", "Closed"]


class RiskMatrixWidget(QTableWidget):
    def __init__(self) -> None:
        super().__init__(5, 5)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.verticalHeader().setVisible(True)
        self.horizontalHeader().setVisible(True)
        self.setFixedHeight(280)
        self.setAlternatingRowColors(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHorizontalHeaderLabels([str(value) for value in range(1, 6)])
        self.setVerticalHeaderLabels([str(value) for value in range(5, 0, -1)])
        for row in range(5):
            for column in range(5):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row, column, item)
        self.refresh([])

    def refresh(self, risks: list[RiskItem]) -> None:
        counts = matrix_counts(risks)
        for visual_row in range(5):
            impact = 5 - visual_row
            for column in range(5):
                likelihood = column + 1
                count = counts.get((impact, likelihood), 0)
                score = impact * likelihood
                item = self.item(visual_row, column)
                item.setText(str(count))
                item.setBackground(_matrix_color(score))


def _matrix_color(score: int) -> Qt.GlobalColor:
    if score <= 5:
        return Qt.GlobalColor.green
    if score <= 10:
        return Qt.GlobalColor.yellow
    if score <= 15:
        return Qt.GlobalColor.darkYellow
    return Qt.GlobalColor.red


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Cyber Risk Assessment Tool")
        self.resize(1380, 860)
        self.risks: list[RiskItem] = load_risks(DATA_PATH)
        self.selected_identifier: str | None = None

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Title", "Category", "Owner", "Residual", "Level", "Status"]
        )
        self.table.itemSelectionChanged.connect(self._load_selected_risk)

        self.total_label = QLabel("0")
        self.critical_label = QLabel("0")
        self.high_label = QLabel("0")
        self.average_label = QLabel("0.0")
        self.matrix = RiskMatrixWidget()

        self.title_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(CATEGORIES)
        self.asset_input = QLineEdit()
        self.scenario_input = QLineEdit()
        self.owner_input = QLineEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(STATUSES)
        self.impact_input = QSpinBox()
        self.impact_input.setRange(1, 5)
        self.likelihood_input = QSpinBox()
        self.likelihood_input.setRange(1, 5)
        self.control_effectiveness_input = QSpinBox()
        self.control_effectiveness_input.setRange(0, 90)
        self.control_effectiveness_input.setSingleStep(10)
        self.notes_input = QTextEdit()
        self.controls_input = QTextEdit()

        self.inherent_score_label = QLabel("1")
        self.residual_score_label = QLabel("1")
        self.level_label = QLabel("Low")

        for widget in (
            self.impact_input,
            self.likelihood_input,
            self.control_effectiveness_input,
        ):
            widget.valueChanged.connect(self._refresh_score_preview)

        self._build_ui()
        self._populate_table()
        self._refresh_dashboard()
        self._refresh_score_preview()

    def _build_ui(self) -> None:
        central = QWidget()
        layout = QHBoxLayout(central)
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(_summary_group(self.total_label, self.critical_label, self.high_label, self.average_label))
        left_layout.addWidget(self.table)

        left_button_row = QHBoxLayout()
        new_button = QPushButton("New risk")
        new_button.clicked.connect(self._new_risk)
        delete_button = QPushButton("Delete selected")
        delete_button.clicked.connect(self._delete_risk)
        load_button = QPushButton("Load ransomware scenario")
        load_button.clicked.connect(self._load_sample_scenario)
        export_button = QPushButton("Export CSV")
        export_button.clicked.connect(self._export_csv)
        for button in (new_button, delete_button, load_button, export_button):
            left_button_row.addWidget(button)
        left_layout.addLayout(left_button_row)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(self._form_group())
        right_layout.addWidget(self._matrix_group())

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar())

        save_action = QAction("Save register", self)
        save_action.triggered.connect(self._save_all)
        self.menuBar().addAction(save_action)

    def _form_group(self) -> QGroupBox:
        group = QGroupBox("Risk details")
        layout = QFormLayout(group)
        layout.addRow("Title", self.title_input)
        layout.addRow("Category", self.category_input)
        layout.addRow("Asset", self.asset_input)
        layout.addRow("Scenario", self.scenario_input)
        layout.addRow("Owner", self.owner_input)
        layout.addRow("Status", self.status_input)
        layout.addRow("Impact (1-5)", self.impact_input)
        layout.addRow("Likelihood (1-5)", self.likelihood_input)
        layout.addRow("Control effectiveness %", self.control_effectiveness_input)
        layout.addRow("Existing controls", self.controls_input)
        layout.addRow("Notes", self.notes_input)

        score_grid = QGridLayout()
        score_grid.addWidget(QLabel("Inherent score"), 0, 0)
        score_grid.addWidget(self.inherent_score_label, 0, 1)
        score_grid.addWidget(QLabel("Residual score"), 1, 0)
        score_grid.addWidget(self.residual_score_label, 1, 1)
        score_grid.addWidget(QLabel("Risk level"), 2, 0)
        score_grid.addWidget(self.level_label, 2, 1)
        layout.addRow(score_grid)

        action_row = QHBoxLayout()
        save_button = QPushButton("Save risk")
        save_button.clicked.connect(self._save_risk)
        clear_button = QPushButton("Clear form")
        clear_button.clicked.connect(self._new_risk)
        action_row.addWidget(save_button)
        action_row.addWidget(clear_button)
        layout.addRow(action_row)
        return group

    def _matrix_group(self) -> QGroupBox:
        group = QGroupBox("Risk matrix")
        layout = QVBoxLayout(group)
        helper = QLabel(
            "Rows show impact from 5 to 1. Columns show likelihood from 1 to 5. "
            "Cell values show how many risks currently sit in each zone."
        )
        helper.setWordWrap(True)
        layout.addWidget(helper)
        layout.addWidget(self.matrix)
        return group

    def _populate_table(self) -> None:
        self.table.setRowCount(len(self.risks))
        for row_index, risk in enumerate(self.risks):
            residual = calculate_residual_score(
                risk.impact, risk.likelihood, risk.control_effectiveness
            )
            level = classify_risk(residual)
            row_values = [
                risk.title,
                risk.category,
                risk.owner,
                str(residual),
                level,
                risk.status,
            ]
            for column, value in enumerate(row_values):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, risk.identifier)
                self.table.setItem(row_index, column, item)
        self.table.resizeColumnsToContents()

    def _refresh_dashboard(self) -> None:
        summary = summarize_risks(self.risks)
        self.total_label.setText(str(summary["total"]))
        self.critical_label.setText(str(summary["critical"]))
        self.high_label.setText(str(summary["high"]))
        self.average_label.setText(str(summary["average_residual_score"]))
        self.matrix.refresh(self.risks)

    def _refresh_score_preview(self) -> None:
        inherent = calculate_inherent_score(
            self.impact_input.value(), self.likelihood_input.value()
        )
        residual = calculate_residual_score(
            self.impact_input.value(),
            self.likelihood_input.value(),
            self.control_effectiveness_input.value(),
        )
        self.inherent_score_label.setText(str(inherent))
        self.residual_score_label.setText(str(residual))
        self.level_label.setText(classify_risk(residual))

    def _new_risk(self) -> None:
        self.selected_identifier = None
        self.title_input.clear()
        self.category_input.setCurrentIndex(0)
        self.asset_input.clear()
        self.scenario_input.clear()
        self.owner_input.clear()
        self.status_input.setCurrentIndex(0)
        self.impact_input.setValue(1)
        self.likelihood_input.setValue(1)
        self.control_effectiveness_input.setValue(0)
        self.controls_input.clear()
        self.notes_input.clear()
        self.table.clearSelection()
        self._refresh_score_preview()

    def _selected_risk(self) -> RiskItem | None:
        if not self.selected_identifier:
            return None
        for risk in self.risks:
            if risk.identifier == self.selected_identifier:
                return risk
        return None

    def _load_selected_risk(self) -> None:
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        identifier = selected_items[0].data(Qt.UserRole)
        self.selected_identifier = str(identifier)
        risk = self._selected_risk()
        if risk is None:
            return
        self.title_input.setText(risk.title)
        self.category_input.setCurrentText(risk.category)
        self.asset_input.setText(risk.asset)
        self.scenario_input.setText(risk.scenario)
        self.owner_input.setText(risk.owner)
        self.status_input.setCurrentText(risk.status)
        self.impact_input.setValue(risk.impact)
        self.likelihood_input.setValue(risk.likelihood)
        self.control_effectiveness_input.setValue(risk.control_effectiveness)
        self.controls_input.setPlainText(risk.existing_controls)
        self.notes_input.setPlainText(risk.notes)
        self._refresh_score_preview()

    def _save_risk(self) -> None:
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Missing title", "Please enter a title for the risk.")
            return

        payload = RiskItem(
            identifier=self.selected_identifier or RiskItem(
                title="",
                category="Operational",
                asset="",
                scenario="",
                owner="",
                status="Open",
                impact=1,
                likelihood=1,
                control_effectiveness=0,
            ).identifier,
            title=self.title_input.text().strip(),
            category=self.category_input.currentText(),
            asset=self.asset_input.text().strip(),
            scenario=self.scenario_input.text().strip(),
            owner=self.owner_input.text().strip(),
            status=self.status_input.currentText(),
            impact=self.impact_input.value(),
            likelihood=self.likelihood_input.value(),
            control_effectiveness=self.control_effectiveness_input.value(),
            notes=self.notes_input.toPlainText().strip(),
            existing_controls=self.controls_input.toPlainText().strip(),
        )

        existing = self._selected_risk()
        if existing is None:
            self.risks.append(payload)
            self.selected_identifier = payload.identifier
        else:
            index = self.risks.index(existing)
            self.risks[index] = payload

        self._save_all()
        self._populate_table()
        self._refresh_dashboard()
        self.statusBar().showMessage("Risk saved", 3000)

    def _delete_risk(self) -> None:
        risk = self._selected_risk()
        if risk is None:
            QMessageBox.information(self, "Nothing selected", "Select a risk first.")
            return
        self.risks = [item for item in self.risks if item.identifier != risk.identifier]
        self._new_risk()
        self._save_all()
        self._populate_table()
        self._refresh_dashboard()
        self.statusBar().showMessage("Risk deleted", 3000)

    def _load_sample_scenario(self) -> None:
        scenario_risks = load_scenario(SCENARIO_PATH)
        self.risks = scenario_risks
        self._new_risk()
        self._save_all()
        self._populate_table()
        self._refresh_dashboard()
        self.statusBar().showMessage("Ransomware scenario loaded", 3000)

    def _export_csv(self) -> None:
        export_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export risk register",
            str(PROJECT_ROOT / "data" / "exports" / "risk-register.csv"),
            "CSV Files (*.csv)",
        )
        if not export_path:
            return
        export_csv(Path(export_path), self.risks)
        self.statusBar().showMessage(f"Exported CSV to {export_path}", 5000)

    def _save_all(self) -> None:
        save_risks(DATA_PATH, self.risks)


def _summary_group(
    total_label: QLabel,
    critical_label: QLabel,
    high_label: QLabel,
    average_label: QLabel,
) -> QGroupBox:
    group = QGroupBox("Register summary")
    layout = QGridLayout(group)
    labels = [
        ("Total risks", total_label),
        ("Critical", critical_label),
        ("High", high_label),
        ("Average residual", average_label),
    ]
    for index, (title, label) in enumerate(labels):
        layout.addWidget(QLabel(title), 0, index)
        label.setStyleSheet("font-size: 22px; font-weight: 600;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, index)
    return group


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv
    app = QApplication(argv)
    window = MainWindow()

    if "--smoke-test" in argv:
        print("cyber-risk-tool-smoke-test: ok")
        return 0

    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
