from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('source_inventory', ROOT / 'tools/source_inventory.py')
source_inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source_inventory)


class SourceInventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.source = Path(self.tmp.name)
        (self.source / '.cursor-plugin').mkdir()
        (self.source / '.cursor-plugin/plugin.json').write_text('{"version":"fixture"}\n')
        (self.source / 'skills/new').mkdir(parents=True)
        (self.source / 'skills/new/SKILL.md').write_text('A complete fixture skill.\n')
        self.previous = {'files': [{'source': '.cursor-plugin/plugin.json', 'destination': 'pstack.json'}]}

    def load(self, **kwargs):
        return source_inventory.inventory(self.source, self.previous, version=kwargs.get('version', 'fixture'),
                                          revision='fixture-revision',
                                          subtree=kwargs.get('subtree', source_inventory.tree_hash(self.source).hex()))

    def test_new_skill_is_accounted_for_without_source_execution(self):
        record = self.load()
        self.assertEqual(record['version'], 'fixture')
        self.assertEqual(record['revision'], 'fixture-revision')
        self.assertEqual([(item['source'], item['destination']) for item in record['files']],
                         [('.cursor-plugin/plugin.json', 'pstack.json'),
                          ('skills/new/SKILL.md', '.agents/skills/new/SKILL.md')])

    def test_changed_bytes_modes_and_version_are_rejected(self):
        digest = source_inventory.tree_hash(self.source).hex()
        skill = self.source / 'skills/new/SKILL.md'
        skill.write_text('Changed source.\n')
        with self.assertRaisesRegex(ValueError, 'Source tree mismatch'):
            self.load(subtree=digest)
        digest = source_inventory.tree_hash(self.source).hex()
        skill.chmod(0o755)
        with self.assertRaisesRegex(ValueError, 'Source tree mismatch'):
            self.load(subtree=digest)
        with self.assertRaisesRegex(ValueError, 'manifest version'):
            self.load(version='different')

    def test_new_non_skill_file_needs_explicit_mapping(self):
        (self.source / 'unknown.md').write_text('New metadata.\n')
        with self.assertRaisesRegex(ValueError, 'explicit destination'):
            self.load()

    def test_source_symlink_is_rejected(self):
        (self.source / 'linked').symlink_to('skills/new/SKILL.md')
        with self.assertRaisesRegex(ValueError, 'Source symlink'):
            self.load()

    def test_change_records_distinguish_addition_removal_and_modification(self):
        def item(name, digest):
            return {'source': name, 'source_sha256': digest, 'destination': name}
        records = source_inventory.changes({'files': [item('a', 'old'), item('b', 'removed')]},
                                          {'files': [item('a', 'new'), item('c', 'added')]})
        self.assertEqual([(r['source'], r['status'], r['before_sha256'], r['after_sha256']) for r in records],
                         [('a', 'modified', 'old', 'new'), ('b', 'removed', 'removed', None),
                          ('c', 'added', None, 'added')])
