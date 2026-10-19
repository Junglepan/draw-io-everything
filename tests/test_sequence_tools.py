"""Failure-path checks: never accept unverified JARs or stale/error previews."""
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_sequence import ensure_jar
from check_sequence import check


class SequenceToolTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.cache').mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT / '.cache')
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.runtime = {'version': 'test', 'url': 'https://example.invalid/never-requested',
                        'sha512': hashlib.sha512(b'trusted').hexdigest()}

    def test_corrupt_cached_jar_is_rejected_without_network(self):
        (self.directory / 'plantuml-test.jar').write_bytes(b'corrupt')
        with patch('render_sequence.urlopen') as download:
            with self.assertRaisesRegex(ValueError, 'Cached JAR checksum mismatch'):
                ensure_jar(self.directory, self.runtime)
            download.assert_not_called()

    def test_bad_download_is_not_installed(self):
        with patch('render_sequence.urlopen', return_value=io.BytesIO(b'corrupt')):
            with self.assertRaisesRegex(ValueError, 'Downloaded JAR checksum mismatch'):
                ensure_jar(self.directory, self.runtime)
        self.assertFalse((self.directory / 'plantuml-test.jar').exists())

    def rejected_render(self, content):
        source = self.directory / 'broken.puml'
        source.write_text(content, encoding='utf-8')
        output = self.directory / 'rendered'
        output.mkdir()
        marker = output / 'previous.png'
        marker.write_bytes(b'previous result')
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/render_sequence.py'),
             '--output-dir', str(output), str(source)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('Command failed', result.stdout)
        self.assertEqual(list(output.iterdir()), [marker])
        self.assertEqual(marker.read_bytes(), b'previous result')

    def test_syntax_error_produces_no_success_manifest_or_error_preview(self):
        self.rejected_render('@startuml\nAlice -> Bob : hello\nINVALID TOKEN {{{\n@enduml\n')

    def test_zero_diagram_run_is_rejected(self):
        self.rejected_render('No diagram here.\n')

    def test_tampered_preview_cannot_pass_saved_manifest(self):
        output = self.directory / 'rendered'
        shutil.copytree(ROOT / 'examples/sequence/rendered', output)
        manifest = json.loads((output / 'render-manifest.json').read_text())
        preview = output / manifest['cases'][0]['artifacts']['svg']['path']
        preview.write_bytes(preview.read_bytes() + b'<!-- changed -->')
        with self.assertRaisesRegex(ValueError, 'Preview hash mismatch'):
            check(output)


if __name__ == '__main__':
    unittest.main()
