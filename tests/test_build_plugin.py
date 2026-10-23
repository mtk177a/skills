import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

BUILDER = Path(__file__).resolve().parents[1] / 'scripts' / 'build_plugin.py'


class PluginBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'source'
        self.root.mkdir()
        self.output = Path(self.temp.name) / 'output'
        self.git('init', '-q')
        self.git('config', 'user.email', 'test@example.com')
        self.git('config', 'user.name', 'Test')
        self.write('plugin.json', json.dumps({'$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'name': 'fixture', 'version': '0.1.0', 'description': 'Fixture', 'author': {'name': 'Test'}, 'license': 'MIT'}))
        self.write('LICENSE', 'MIT fixture')
        self.write('THIRD_PARTY_NOTICES.md', 'Fixture notices')
        self.write('skills/example/SKILL.md', '---\nname: example\ndescription: Example\nlicense: MIT\n---\nRead [guide](references/guide.md).\n')
        self.write('skills/example/references/guide.md', '# Guide\n')
        self.write('skills/example/SKILL-ja.md', 'reference translation')
        self.write('.agents/skills/private/SKILL.md', 'not distributed')
        self.commit()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.STDOUT).decode().strip()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')
        return self.git('rev-parse', 'HEAD')

    def build(self, ref='HEAD', output=None):
        return subprocess.run([sys.executable, '-B', str(BUILDER), '--repo', str(self.root), '--ref', ref, '--output-dir', str(output or self.output)], capture_output=True, text=True)

    def test_fixed_commit_preserves_bytes_and_excludes_non_runtime_files(self):
        commit = self.git('rev-parse', 'HEAD')
        original = (self.root / 'skills/example/SKILL.md').read_bytes()
        self.write('skills/example/SKILL.md', 'uncommitted edit')
        self.write('skills/untracked/SKILL.md', 'untracked')
        result = self.build(commit)
        self.assertEqual(result.returncode, 0, result.stderr)
        with zipfile.ZipFile(self.output / 'fixture-0.1.0.zip') as archive:
            self.assertEqual(set(archive.namelist()), {'plugin.json', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'skills/example/SKILL.md', 'skills/example/references/guide.md'})
            self.assertEqual(archive.read('skills/example/SKILL.md'), original)
        record = json.loads((self.output / 'fixture-0.1.0.build.json').read_text())
        self.assertEqual(record['source_commit'], commit)
        self.assertEqual(record['skills'], ['example'])

    def test_missing_packaged_reference_fails_before_output(self):
        self.write('skills/example/references/guide.md', 'Read [translation](../SKILL-ja.md).')
        self.commit()
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing packaged reference', result.stderr)
        self.assertFalse(self.output.exists())

    def test_changed_mirror_is_rejected(self):
        self.write('skills/japanese-tech-writing/SKILL.md', 'changed mirror')
        self.write('skills/japanese-tech-writing/UPSTREAM.md', 'SKILL.md SHA-256: `sha256:' + '0' * 64 + '`')
        self.commit()
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('mirror hash', result.stderr)

    def test_reproducible_archive_and_no_overwrite(self):
        self.assertEqual(self.build().returncode, 0)
        other = Path(self.temp.name) / 'second'
        self.assertEqual(self.build(output=other).returncode, 0)
        for name in ('fixture-0.1.0.zip', 'fixture-0.1.0.build.json', 'fixture-0.1.0.sha256'):
            self.assertEqual((self.output / name).read_bytes(), (other / name).read_bytes())
        original = (self.output / 'fixture-0.1.0.zip').read_bytes()
        self.assertNotEqual(self.build().returncode, 0)
        self.assertEqual((self.output / 'fixture-0.1.0.zip').read_bytes(), original)

    def test_missing_companion_code_reference_is_rejected(self):
        self.write('skills/example/SKILL.md', 'Read `../companion/SKILL.md` before use.')
        self.commit()
        self.assertIn('missing packaged reference', self.build().stderr)

    def test_symlink_is_not_followed(self):
        (self.root / 'skills/example/references/link.md').symlink_to('/etc/passwd')
        self.commit()
        self.assertIn('only regular files', self.build().stderr)

    def test_manifest_schema_and_unsafe_name_are_rejected(self):
        for field, value in (('$schema', 'unsupported'), ('name', '../escape'), ('version', '../escape')):
            with self.subTest(field=field):
                path = self.root / 'plugin.json'
                original = path.read_text()
                document = json.loads(original)
                document[field] = value
                path.write_text(json.dumps(document))
                self.commit()
                self.assertNotEqual(self.build().returncode, 0)
                path.write_text(original)

    def test_missing_license_and_skill_entrypoint_are_rejected(self):
        (self.root / 'LICENSE').unlink()
        self.commit()
        self.assertIn('missing required files', self.build().stderr)
        self.write('LICENSE', 'MIT fixture')
        (self.root / 'skills/example/SKILL.md').unlink()
        self.commit()
        self.assertIn('missing SKILL.md', self.build().stderr)

    def test_parent_escape_is_rejected(self):
        self.write('skills/example/SKILL.md', '[outside](../../../secret.md)')
        self.commit()
        self.assertIn('escapes package', self.build().stderr)

    def test_executable_resource_mode_is_preserved(self):
        self.write('skills/example/scripts/run.sh', '#!/bin/sh\necho example\n')
        (self.root / 'skills/example/scripts/run.sh').chmod(0o755)
        self.commit()
        self.assertEqual(self.build().returncode, 0)
        with zipfile.ZipFile(self.output / 'fixture-0.1.0.zip') as archive:
            self.assertEqual(archive.getinfo('skills/example/scripts/run.sh').external_attr >> 16, 0o100755)

    def test_submodule_skill_is_rejected_instead_of_silently_omitted(self):
        commit = self.git('rev-parse', 'HEAD')
        self.git('update-index', '--add', '--cacheinfo', f'160000,{commit},skills/nested')
        self.git('commit', '-qm', 'add nested Skill')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('only regular files', result.stderr)


if __name__ == '__main__':
    unittest.main()
