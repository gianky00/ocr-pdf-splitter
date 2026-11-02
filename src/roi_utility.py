"""
Intelleo PDF Splitter - ROI Drawing Utility
Strumento standalone per definire le Regioni di Interesse (ROI) sui documenti PDF.
"""

import logging
import sys
from typing import Any

from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsScene,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from config_manager import ConfigManager
from core.pdf_manager import PdfManager
from core.roi_manager import RoiManager
from core.rule_service import RuleService
from gui.widgets.pdf_graphics_view import ROIGraphicsView
from gui.widgets.roi_renderer import ROIRenderer

logger = logging.getLogger("ROI_UTILITY")

_ROI_MARKER_KEY = 11
_ROI_RULE_KEY = 12
_ROI_INDEX_KEY = 13


def _roi_coords(coords: Any) -> list[int] | None:
    """Normalizza una ROI in quattro interi PDF, oppure None se non è valida."""
    if not isinstance(coords, (list, tuple)) or len(coords) != 4:
        return None
    try:
        return [int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])]
    except (TypeError, ValueError):
        return None


def _fitz_pixmap_to_qpixmap(pix: Any) -> QPixmap:
    """Converte una pixmap PyMuPDF in QPixmap, copiando il buffer."""
    if pix.alpha or pix.n == 4:
        image_format = QImage.Format.Format_RGBA8888
    elif pix.n == 1:
        image_format = QImage.Format.Format_Grayscale8
    else:
        image_format = QImage.Format.Format_RGB888
    image = QImage(pix.samples, pix.width, pix.height, pix.stride, image_format)
    return QPixmap.fromImage(image.copy())


class ROIDrawingApp(QMainWindow):
    """
    Applicazione per il disegno e la gestione delle ROI.
    Permette di caricare un PDF e tracciare rettangoli da associare alle regole.
    """

    def __init__(self) -> None:
        """Inizializza l'utility ROI, carica le regole e configura la UI."""
        super().__init__()
        self.config = ConfigManager.load_config()
        self.rule_service = RuleService(self.config)
        self.roi_manager = RoiManager()
        self.pdf_manager = PdfManager()

        self.current_pdf_path: str | None = None
        self.current_page = 0
        self.rules: list[dict[str, Any]] = self.rule_service.get_rules()
        self.selected_rule_name: str | None = None
        self.delete_mode = False

        self.setWindowTitle("Intelleo PDF Splitter - Gestione Regole e ROI")
        self.resize(1400, 900)

        self.setup_ui()
        self._update_rules_list()

    def setup_ui(self) -> None:
        """Configura il layout principale e i pannelli laterali."""
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.left_panel = QWidget()
        self.left_panel.setFixedWidth(300)
        self.left_layout = QVBoxLayout(self.left_panel)
        self.lbl_rules = QLabel("<b>Regole di Classificazione</b>")
        self.left_layout.addWidget(self.lbl_rules)
        self.list_rules = QListWidget()
        self.list_rules.currentRowChanged.connect(self.on_rule_selected)
        self.left_layout.addWidget(self.list_rules)
        self.main_layout.addWidget(self.left_panel)

        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)

        # Attributi minimi richiesti da ROIGraphicsView
        self.zoom_level = 1.0
        self.status_bar = QLabel("Pronto")
        self.right_layout.addWidget(self.status_bar)

        if getattr(sys, "_testing", False):
            from unittest.mock import MagicMock

            self.view: Any = MagicMock()
            self.scene: Any = MagicMock()
            self.right_layout.addWidget(QWidget())
        else:
            self.scene = QGraphicsScene()
            self.view = ROIGraphicsView(app=self, parent=None)
            self.view.setScene(self.scene)
            self.right_layout.addWidget(self.view)

        self.main_layout.addWidget(self.right_panel)
        self.setup_toolbar()

    def setup_toolbar(self) -> None:
        """Crea la barra degli strumenti con le azioni principali."""
        self.toolbar = QToolBar("Tools")
        self.addToolBar(self.toolbar)
        self.btn_open = QAction("Apri PDF", self)
        self.btn_open.triggered.connect(self.open_pdf)
        self.toolbar.addAction(self.btn_open)
        self.toolbar.addSeparator()
        self.btn_delete = QAction("Modalità Elimina", self)
        self.btn_delete.setCheckable(True)
        self.btn_delete.triggered.connect(self.toggle_delete_mode)
        self.toolbar.addAction(self.btn_delete)

    def open_pdf(self) -> None:
        """Apre il selettore file per scegliere il PDF di riferimento."""
        path, _ = QFileDialog.getOpenFileName(self, "Apri PDF", "", "PDF Files (*.pdf)")
        if path:
            self.current_pdf_path = path
            self.load_page(0)

    def load_page(self, page_num: int) -> None:
        """Carica e renderizza la pagina specificata del PDF corrente."""
        if not self.current_pdf_path:
            return
        pix = self.pdf_manager.get_page_pixmap(self.current_pdf_path, page_num)
        if not pix:
            return
        qpixmap = _fitz_pixmap_to_qpixmap(pix)
        if qpixmap.isNull():
            return
        self.current_page = page_num
        self.on_page_rendered(qpixmap)

    def on_rule_selected(self, index: int) -> None:
        """Gestisce il cambio della regola attiva per l'associazione ROI."""
        if 0 <= index < len(self.rules):
            self.selected_rule_name = self.rules[index]["category_name"]
            if not getattr(sys, "_testing", False):
                self.view.clear_rois()
                self.show_existing_rois()

    def on_roi_drawn(self, rect: Any) -> None:
        """Callback invocata quando una nuova ROI viene tracciata sulla vista."""

    def show_existing_rois(self) -> None:
        """Visualizza sulla scena le ROI già salvate per la regola corrente."""
        if not hasattr(self.view, "clear_rois"):
            return
        self.view.clear_rois()
        if not self.selected_rule_name:
            return
        scene = self.view.scene()
        if scene is None:
            return

        rules = self.rule_service.get_rules()
        self.rules = rules
        renderer = ROIRenderer(scene, self.zoom_level)
        for rule_index, rule in enumerate(rules):
            if not isinstance(rule, dict) or rule.get("category_name") != self.selected_rule_name:
                continue
            color = str(rule.get("color") or "#0D6EFD")
            category = str(rule.get("category_name") or "")
            rois = rule.get("rois", [])
            if not isinstance(rois, list):
                continue
            for roi_index, coords in enumerate(rois):
                pdf_coords = _roi_coords(coords)
                if pdf_coords is None:
                    continue
                items = renderer.draw_roi(rule_index, roi_index, category, color, pdf_coords)
                for item in items:
                    item.setData(_ROI_MARKER_KEY, 1)
                    item.setData(_ROI_RULE_KEY, rule_index)
                    item.setData(_ROI_INDEX_KEY, roi_index)
                if hasattr(self.view, "track_roi_items"):
                    self.view.track_roi_items(items)

    def handle_delete_click(self, scene_pos: Any) -> None:
        """Elimina la ROI sotto il cursore quando la modalità elimina è attiva."""
        scene = self.view.scene() if hasattr(self.view, "scene") else None
        if scene is None:
            return
        for item in scene.items(scene_pos):
            if item.data(_ROI_MARKER_KEY) != 1:
                continue
            rule_index = item.data(_ROI_RULE_KEY)
            roi_index = item.data(_ROI_INDEX_KEY)
            if isinstance(rule_index, float):
                rule_index = int(rule_index)
            if isinstance(roi_index, float):
                roi_index = int(roi_index)
            if not isinstance(rule_index, int) or not isinstance(roi_index, int):
                continue
            rules = self.rule_service.get_rules()
            if not (0 <= rule_index < len(rules)):
                return
            rois = rules[rule_index].get("rois")
            if not isinstance(rois, list) or not (0 <= roi_index < len(rois)):
                return
            rois.pop(roi_index)
            self.rule_service.save_rules()
            self.rules = rules
            self.show_existing_rois()
            self.status_bar.setText("ROI eliminata")
            return

    def toggle_delete_mode(self, enabled: bool) -> None:
        """Attiva o disattiva la modalità di eliminazione delle ROI."""
        self.delete_mode = enabled
        if not getattr(sys, "_testing", False):
            self.view.set_delete_mode(enabled)

    def _update_rules_list(self) -> None:
        """Aggiorna il widget QListWidget con i nomi delle regole caricate."""
        self.list_rules.clear()
        for rule in self.rules:
            self.list_rules.addItem(rule["category_name"])

    def on_zoom_changed(self, value: int) -> None:
        """Slot per la gestione dello zoom via slider o input numerico."""
        self.zoom_level = value / 100.0
        if not getattr(sys, "_testing", False):
            self.view.set_zoom(self.zoom_level)

    def zoom_in(self) -> None:
        """Incrementa il livello di zoom della vista PDF."""
        self.zoom_level += 0.1
        if not getattr(sys, "_testing", False):
            self.view.set_zoom(self.zoom_level)

    def zoom_out(self) -> None:
        """Riduce il livello di zoom della vista PDF (min 10%)."""
        self.zoom_level = max(0.1, self.zoom_level - 0.1)
        if not getattr(sys, "_testing", False):
            self.view.set_zoom(self.zoom_level)

    def prompt_and_save_roi(self, coords_pdf: list[int]) -> None:
        """Salva i dati della ROI nel gestore regole corrente."""
        if not self.selected_rule_name:
            QMessageBox.warning(self, "Attenzione", "Seleziona una regola a sinistra prima di disegnare.")
            return

        reply = QMessageBox.question(
            self,
            "Conferma",
            f"Salvare questa ROI per '{self.selected_rule_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes and self.rule_service.add_roi_to_rule(
            self.selected_rule_name, coords_pdf
        ):
            self.rule_service.save_rules()
            self.status_bar.setText(f"ROI salvata per {self.selected_rule_name}")
            self.show_existing_rois()

    def on_page_rendered(self, pixmap: QPixmap) -> None:
        """Metodo unificato per il rendering della pixmap sulla vista."""
        if hasattr(self.view, "set_background"):
            self.view.set_background(pixmap)
        self.show_existing_rois()


def run_utility() -> None:
    """Funzione di bootstrap per l'avvio dell'utility ROI standalone."""
    from contextlib import suppress

    import license_updater
    import license_validator

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    with suppress(Exception):
        license_updater.run_update()
    is_valid, _msg = license_validator.verify_license()
    if not is_valid:
        sys.exit(1)
    window = ROIDrawingApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_utility()
