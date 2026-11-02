"""Test per gli import del build e la copia sulla share di rete."""

import logging
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

ADMIN_DIR = Path(__file__).resolve().parents[1] / "admin" / "Crea Setup"


def _load_build_dist():
    """Importa build_dist e ripristina cwd e build_log.txt."""
    cwd = os.getcwd()
    log_path = ADMIN_DIR / "build_log.txt"
    backup = log_path.read_bytes() if log_path.is_file() else None
    if str(ADMIN_DIR) not in sys.path:
        sys.path.insert(0, str(ADMIN_DIR))
    import build_dist

    os.chdir(cwd)
    for handler in logging.root.handlers[:]:
        if isinstance(handler, logging.FileHandler) and Path(handler.baseFilename) == log_path:
            handler.close()
            logging.root.removeHandler(handler)
    if backup is None:
        if log_path.exists():
            log_path.unlink()
    else:
        log_path.write_bytes(backup)
    return build_dist


class TestBuildDist(unittest.TestCase):
    """Copertura degli errori di pacchetto e di deploy di rete."""

    @classmethod
    def setUpClass(cls):
        cls.build_dist = _load_build_dist()

    def test_source_imports_include_uuid(self):
        modules = self.build_dist.source_module_imports(self.build_dist.ROOT_DIR / "src")
        self.assertIn("uuid", modules)

    def test_copy_network_file_overwrites_readonly_destination(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "version.json"
            destination = root / "share" / "version.json"
            source.write_text('{"version": "2.1.50"}', encoding="utf-8")
            destination.parent.mkdir()
            destination.write_text("old", encoding="utf-8")
            os.chmod(destination, stat.S_IREAD)

            self.build_dist.copy_network_file(source, destination)

            self.assertEqual(destination.read_text(encoding="utf-8"), '{"version": "2.1.50"}')
