from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bundle_catalog', ROOT / 'tools/catalog.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CatalogModeTests(unittest.TestCase):
    def test_inventory_matches_the_installers_exact_mode_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            file = root / 'skill.md'
            file.write_text('fixture\n')
            for mode in (0o644, 0o755):
                file.chmod(mode)
                self.assertEqual(module.inventory(root)['files']['skill.md']['mode'], f'{mode:o}')
            for mode in (0o664, 0o600, 0o777):
                file.chmod(mode)
                with self.assertRaisesRegex(ValueError, 'Bundle mode must be 644 or 755'):
                    module.inventory(root)
