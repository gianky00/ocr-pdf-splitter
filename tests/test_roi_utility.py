"""
Unit tests for the ROI Drawing utility.
"""

import sys
import tempfile
import typing
import unittest
from pathlib import Path
from unittest.mock import patch

import pymupdf as fitz
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QMouseEvent, QPixmap
from PySide6.QtWidgets import QApplication, QGraphicsPixmapItem, QGraphicsRectItem, QMessageBox

# Activate testing mode before import
sys._testing = True  # type: ignore
from roi_utility import ROIDrawingApp  # noqa: E402


class TestRoiUtility(unittest.TestCase):
    """Test suite for ROIDrawingApp utility."""

    app: QApplication

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize QApplication for widget tests."""
        cls.app = typing.cast("QApplication", QApplication.instance() or QApplication([]))

    def setUp(self) -> None:
        """Create window and controller mocks."""
        self._testing_present = hasattr(sys, "_testing")
        self._testing_value = getattr(sys, "_testing", None)
        sys._testing = True
        with patch("roi_utility.RuleService"), patch("roi_utility.ConfigManager"):
            self.window = ROIDrawingApp()

    def tearDown(self) -> None:
        """Clean up window."""
        self.window.close()
        if self._testing_present:
            sys._testing = self._testing_value
        elif hasattr(sys, "_testing"):
            delattr(sys, "_testing")

    def test_initialization(self) -> None:
        """Test window title and initial UI state."""
        self.assertIn("Gestione Regole e ROI", self.window.windowTitle())
        self.assertFalse(self.window.delete_mode)

    def test_toggle_delete_mode(self) -> None:
        """Test switching between drawing and deletion modes."""
        self.window.toggle_delete_mode(True)
        self.assertTrue(self.window.delete_mode)

        self.window.toggle_delete_mode(False)
        self.assertFalse(self.window.delete_mode)

    def test_on_zoom_changed(self) -> None:
        """Test zoom level updates from the UI slider."""
        self.window.on_zoom_changed(150)
        # Check if no crash

    def test_on_page_rendered(self) -> None:
        """Test handling of background image rendering."""
        pixmap = QPixmap(100, 100)
        # Se siamo in test, self.window.view è un MagicMock
        self.window.on_page_rendered(pixmap)
        # Verifichiamo che set_background sia stato chiamato sul mock del view
        if hasattr(self.window.view, "set_background"):
            self.window.view.set_background.assert_called()

    def test_update_rules_list(self) -> None:
        """Test population of the rules list widget."""
        self.window.rules = [{"category_name": "Rule1"}]
        self.window._update_rules_list()
        self.assertEqual(self.window.list_rules.count(), 1)

    def test_load_page_shows_pdf_on_visible_scene(self) -> None:
        """La pagina aperta deve comparire sulla scena collegata alla vista."""
        window = None
        previous_testing = getattr(sys, "_testing", False)
        with tempfile.TemporaryDirectory() as tmp:
            pdf_path = Path(tmp) / "page.pdf"
            document = fitz.open()
            page = document.new_page(width=200, height=120)
            page.insert_text((20, 40), "ROI")
            document.save(pdf_path)
            document.close()

            sys._testing = False
            try:
                with patch("roi_utility.RuleService") as rule_service, patch("roi_utility.ConfigManager") as config:
                    config.load_config.return_value = {}
                    rule_service.return_value.get_rules.return_value = []
                    window = ROIDrawingApp()
                window.current_pdf_path = str(pdf_path)
                window.load_page(0)

                scene = window.view.scene()
                self.assertIsNotNone(scene)
                pixmaps = [item for item in scene.items() if isinstance(item, QGraphicsPixmapItem)]
                self.assertEqual(len(pixmaps), 1)
                self.assertFalse(pixmaps[0].pixmap().isNull())
                self.assertGreater(pixmaps[0].pixmap().width(), 0)
                self.assertGreater(pixmaps[0].pixmap().height(), 0)
            finally:
                if window is not None:
                    window.pdf_manager.close()
                    window.close()
                sys._testing = previous_testing

    def test_load_page_missing_pdf_leaves_scene_empty(self) -> None:
        """Un percorso inesistente non deve disegnare nulla né sollevare eccezioni."""
        window = None
        previous_testing = getattr(sys, "_testing", False)
        sys._testing = False
        try:
            with patch("roi_utility.RuleService") as rule_service, patch("roi_utility.ConfigManager") as config:
                config.load_config.return_value = {}
                rule_service.return_value.get_rules.return_value = []
                window = ROIDrawingApp()
            window.current_pdf_path = str(Path(tempfile.gettempdir()) / "pdf-inesistente-roi.pdf")
            window.load_page(0)
            scene = window.view.scene()
            self.assertIsNotNone(scene)
            pixmaps = [item for item in scene.items() if isinstance(item, QGraphicsPixmapItem)]
            self.assertEqual(pixmaps, [])
        finally:
            if window is not None:
                window.pdf_manager.close()
                window.close()
            sys._testing = previous_testing

    def _open_real_window(self, rules: list[dict]) -> tuple[ROIDrawingApp, list]:
        """Apre la finestra reale e lascia attivi i patch fino a stop esplicito."""
        config = {"classification_rules": rules}
        patches = [
            patch("roi_utility.ConfigManager.load_config", return_value=config),
            patch("config_manager.save_config"),
        ]
        for item in patches:
            item.start()
        return ROIDrawingApp(), patches

    def _close_real_window(self, window: ROIDrawingApp | None, patches: list) -> None:
        """Chiude la finestra e rimuove i patch prima di toccare il config reale."""
        if window is not None:
            window.close()
        for item in patches:
            item.stop()

    def test_saved_roi_stays_visible_after_yes(self) -> None:
        """Dopo Yes il rettangolo resta sull'anteprima, sopra il PDF."""
        window = None
        patches: list = []
        previous_testing = getattr(sys, "_testing", False)
        sys._testing = False
        try:
            window, patches = self._open_real_window([{"category_name": "prova", "color": "#0D6EFD", "rois": []}])
            window.view.set_background(QPixmap(400, 300))
            window.on_rule_selected(0)
            with patch("roi_utility.QMessageBox.question", return_value=QMessageBox.StandardButton.Yes):
                window.prompt_and_save_roi([72, 36, 144, 108])

            scene = window.view.scene()
            self.assertIsNotNone(scene)
            pixmaps = [item for item in scene.items() if isinstance(item, QGraphicsPixmapItem)]
            rects = [item for item in scene.items() if isinstance(item, QGraphicsRectItem)]
            self.assertEqual(len(pixmaps), 1)
            roi_rects = [item for item in rects if item.rect().height() > 18]
            self.assertEqual(len(roi_rects), 1)
            self.assertAlmostEqual(roi_rects[0].rect().x(), 150.0, delta=0.5)
            self.assertAlmostEqual(roi_rects[0].rect().y(), 75.0, delta=0.5)
            self.assertAlmostEqual(roi_rects[0].rect().width(), 150.0, delta=0.5)
            self.assertAlmostEqual(roi_rects[0].rect().height(), 150.0, delta=0.5)
            self.assertEqual(window.rules[0]["rois"], [[72, 36, 144, 108]])
        finally:
            self._close_real_window(window, patches)
            sys._testing = previous_testing

    def test_selecting_rule_shows_existing_rois(self) -> None:
        """Selezionare una regola ridisegna le ROI già salvate senza togliere il PDF."""
        window = None
        patches: list = []
        previous_testing = getattr(sys, "_testing", False)
        sys._testing = False
        try:
            window, patches = self._open_real_window(
                [{"category_name": "prova", "color": "#0D6EFD", "rois": [[72, 36, 144, 108]]}]
            )
            window.view.set_background(QPixmap(400, 300))
            window.on_rule_selected(0)
            scene = window.view.scene()
            self.assertIsNotNone(scene)
            self.assertEqual(len([item for item in scene.items() if isinstance(item, QGraphicsPixmapItem)]), 1)
            roi_rects = [
                item for item in scene.items() if isinstance(item, QGraphicsRectItem) and item.rect().height() > 18
            ]
            self.assertEqual(len(roi_rects), 1)
        finally:
            self._close_real_window(window, patches)
            sys._testing = previous_testing

    def test_delete_click_removes_roi_and_empty_click_is_safe(self) -> None:
        """In modalità elimina un click sulla ROI la toglie; un click vuoto non solleva errori."""
        window = None
        patches: list = []
        previous_testing = getattr(sys, "_testing", False)
        sys._testing = False
        try:
            window, patches = self._open_real_window(
                [{"category_name": "prova", "color": "#0D6EFD", "rois": [[72, 36, 144, 108]]}]
            )
            window.view.set_background(QPixmap(400, 300))
            window.on_rule_selected(0)
            window.handle_delete_click(QPointF(-20, -20))
            self.assertEqual(window.rules[0]["rois"], [[72, 36, 144, 108]])

            window.delete_mode = True
            pos = QPointF(10, 10)
            event = QMouseEvent(
                QMouseEvent.Type.MouseButtonPress,
                pos,
                pos,
                pos,
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier,
            )
            window.view.mousePressEvent(event)

            window.handle_delete_click(QPointF(200, 150))
            self.assertEqual(window.rules[0]["rois"], [])
            scene = window.view.scene()
            self.assertIsNotNone(scene)
            roi_rects = [
                item for item in scene.items() if isinstance(item, QGraphicsRectItem) and item.rect().height() > 18
            ]
            self.assertEqual(roi_rects, [])
            self.assertEqual(len([item for item in scene.items() if isinstance(item, QGraphicsPixmapItem)]), 1)
        finally:
            self._close_real_window(window, patches)
            sys._testing = previous_testing


if __name__ == "__main__":
    unittest.main()
