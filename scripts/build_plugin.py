#!/usr/bin/env python3
"""Build a portable Skills plugin from committed Git blobs, without installing it."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import posixpath
import re
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

from check_repository import INLINE_LINK, REFERENCE_LINK, markdown_without_code, link_destination, is_external_link, UPSTREAM_MIRRORS

SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
ROOT_FILES = {'plugin.json', 'LICENSE', 'THIRD_PARTY_NOTICES.md'}


class BuildError(ValueError):
    pass


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True)
    if result.returncode:
        raise BuildError(result.stderr.decode(errors='replace').strip())
    return result.stdout


def included(name: str) -> bool:
    if name in ROOT_FILES:
        return True
    parts = PurePosixPath(name).parts
    return (len(parts) >= 3 and parts[0] == 'skills'
            and 'evals' not in parts[2:]
            and not parts[-1].endswith(('-ja.md', '.ja.md')))


def source_files(repo: Path, ref: str) -> tuple[str, dict[str, tuple[str, bytes]]]:
    commit = git(repo, 'rev-parse', '--verify', '--end-of-options', ref + '^{commit}').decode().strip()
    files = {}
    for entry in git(repo, 'ls-tree', '-rz', '--full-tree', commit).split(b'\0'):
        if not entry:
            continue
        meta, raw_name = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = raw_name.decode('utf-8')
        if kind == 'commit' and name.startswith('skills/') and '/evals/' not in name:
            raise BuildError(f'{name}: only regular files are supported (submodule)')
        if not included(name):
            continue
        if mode not in {'100644', '100755'} or kind != 'blob':
            raise BuildError(f'{name}: only regular files are supported (mode {mode})')
        if '\\' in name or any(part in {'', '.', '..'} for part in name.split('/')):
            raise BuildError(f'{name}: unsafe archive path')
        files[name] = (mode, git(repo, 'cat-file', 'blob', oid))
    return commit, files


def validate_references(files: dict[str, tuple[str, bytes]]) -> None:
    for name, (_, data) in files.items():
        if not name.endswith('.md'):
            continue
        text = data.decode('utf-8')
        visible = markdown_without_code(text)
        destinations = [link_destination(m.group(1)) for pattern in (INLINE_LINK, REFERENCE_LINK) for m in pattern.finditer(visible)]
        # Prose code spans used by this catalog for mandatory runtime resources.
        # Generic file examples and target-repository instructions require manual review.
        destinations += re.findall(r'`((?:references/|\.\./)[^`\n]+)`', text)
        for destination in destinations:
            if is_external_link(destination):
                continue
            clean = unquote(destination.split('#', 1)[0].split('?', 1)[0])
            target = posixpath.normpath(posixpath.join(posixpath.dirname(name), clean))
            if target.startswith('../') or target == '..' or '\\' in target:
                raise BuildError(f'{name}: reference escapes package: {destination}')
            if target not in files and not any(p.startswith(target.rstrip('/') + '/') for p in files):
                raise BuildError(f'{name}: missing packaged reference: {destination}')


def validate(files: dict[str, tuple[str, bytes]]) -> dict:
    missing = ROOT_FILES - files.keys()
    if missing:
        raise BuildError(f'missing required files: {sorted(missing)}')
    manifest = json.loads(files['plugin.json'][1])
    if not isinstance(manifest, dict) or manifest.get('$schema') != SCHEMA:
        raise BuildError('plugin.json: expected Agent Plugins 1.0.0 schema')
    for field in ('name', 'version', 'description'):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            raise BuildError(f'plugin.json: {field} must be a nonempty string')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', manifest['name']):
        raise BuildError('plugin.json: name must use kebab-case')
    if not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', manifest['version']):
        raise BuildError('plugin.json: this release builder requires a stable x.y.z version')
    skills = sorted({name.split('/')[1] for name in files if name.startswith('skills/')})
    if not skills:
        raise BuildError('no Skills found')
    for skill in skills:
        if f'skills/{skill}/SKILL.md' not in files:
            raise BuildError(f'{skill}: missing SKILL.md')
    for skill in UPSTREAM_MIRRORS:
        path = f'skills/{skill}/SKILL.md'
        if path not in files:
            continue
        provenance = files.get(f'skills/{skill}/UPSTREAM.md')
        match = re.search(r'SKILL\.md SHA-256: `sha256:([0-9a-f]{64})`', provenance[1].decode()) if provenance else None
        if not match or hashlib.sha256(files[path][1]).hexdigest() != match.group(1):
            raise BuildError(f'{skill}: mirror hash does not match UPSTREAM.md')
    validate_references(files)
    return manifest


def archive_bytes(files: dict[str, tuple[str, bytes]]) -> bytes:
    buffer = io.BytesIO()
    # Stored entries avoid compression-library/version differences in repeated builds.
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name, (mode, content) in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = int(mode, 8) << 16
            archive.writestr(entry, content)
    result = buffer.getvalue()
    with zipfile.ZipFile(io.BytesIO(result)) as archive:
        if set(archive.namelist()) != set(files):
            raise BuildError('archive file list differs from selected source')
        for name, (mode, content) in files.items():
            if archive.read(name) != content or archive.getinfo(name).external_attr >> 16 != int(mode, 8):
                raise BuildError(f'{name}: archive content or mode differs from source')
    return result


def build(repo: Path, ref: str, output: Path) -> Path:
    commit, files = source_files(repo, ref)
    manifest = validate(files)
    content = archive_bytes(files)
    stem = f"{manifest['name']}-{manifest['version']}"
    record = {
        'name': manifest['name'], 'version': manifest['version'], 'source_commit': commit,
        'archive': stem + '.zip', 'sha256': hashlib.sha256(content).hexdigest(),
        'skills': sorted({p.split('/')[1] for p in files if p.startswith('skills/')}),
        'files': {p: {'mode': mode, 'sha256': hashlib.sha256(data).hexdigest()} for p, (mode, data) in sorted(files.items())},
    }
    outputs = {stem + '.zip': content,
               stem + '.sha256': (record['sha256'] + '  ' + stem + '.zip\n').encode(),
               stem + '.build.json': (json.dumps(record, indent=2, ensure_ascii=False) + '\n').encode()}
    output.mkdir(parents=True, exist_ok=True)
    for name in outputs:
        if (output / name).exists():
            raise BuildError(f'{output / name}: already exists; use a new output directory')
    for name, data in outputs.items():
        with (output / name).open('xb') as handle:
            handle.write(data)
    return output / (stem + '.zip')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--ref', required=True, help='Commit or ref; resolved once to a commit')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(build(args.repo, args.ref, args.output_dir))
    except (BuildError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f'build failed: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
