"""
Unit tests for the application controller.
"""

import typing
import unittest
from unittest.mock import MagicMock, patch

from PySide6.QtCore import QCoreApplication

from core.app_controller import AppController


class TestAppController(unittest.TestCase):
    """Test suite for AppController class."""

    app: QCoreApplication

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize QCoreApplication for signals."""
        cls.app = typing.cast("QCoreApplication", QCoreApplication.instance() or QCoreApplication([]))

    def setUp(self) -> None:
        """Create controller instance with mocked dependencies."""
        with patch("core.app_controller.ConfigManager"), patch("core.app_controller.RuleService"):
            self.controller = AppController()

    def test_load_settings(self) -> None:
        """Test loading settings."""
        self.controller.load_settings()
        self.assertIsNotNone(self.controller.config)

    def test_set_pdf_files(self) -> None:
        """Test setting PDF file list."""
        with patch("core.app_controller.FileService.find_pdfs_in_path", return_value=["test.pdf"]):
            self.controller.set_pdf_files(["dummy_path"])
            self.assertEqual(len(self.controller.pdf_files), 1)

    @patch("core.app_controller.license_validator.get_license_info", return_value={"Cliente": "Test"})
    @patch("core.app_controller.license_validator.get_hardware_id", return_value="HWID")
    @patch("core.app_controller.ConfigManager.load_config", return_value={})
    def test_check_license(self, mock_cfg, mock_hw, mock_lic) -> None:
        """Test license verification."""
        mock_slot = MagicMock()
        self.controller.license_status_updated.connect(mock_slot)
        self.controller.check_license()
        mock_slot.assert_called_once()

    @patch("core.app_controller.ProcessingWorker")
    def test_start_processing(self, mock_worker) -> None:
        """Test starting the processing worker."""
        self.controller.pdf_files = ["test.pdf"]
        res = self.controller.start_processing("ODC123")
        self.assertTrue(res)

    @patch("core.app_controller.ProcessingWorker")
    def test_start_processing_non_controlla_la_licenza(self, mock_worker) -> None:
        """L'avvio elaborazione non ricontrolla la licenza: il controllo resta all'avvio."""
        self.controller.pdf_files = ["test.pdf"]
        messages: list[str] = []
        self.controller.log_received.connect(lambda msg, _level, _replace: messages.append(msg))
        with (
            patch.object(self.controller, "check_license_online") as online,
            patch.object(self.controller, "check_license") as local,
        ):
            res = self.controller.start_processing("ODC123")
        self.assertTrue(res)
        online.assert_not_called()
        local.assert_not_called()
        self.assertNotIn("Verifica autorizzazioni in corso...", messages)
        mock_worker.return_value.start.assert_called_once()

    def test_process_log_queue(self) -> None:
        """Test log queue processing."""
        self.controller.log_queue.put(("Test log", "INFO"))
        mock_slot = MagicMock()
        self.controller.log_received.connect(mock_slot)
        self.controller.process_log_queue()
        mock_slot.assert_called_once_with("Test log", "INFO", False)


if __name__ == "__main__":
    unittest.main()
