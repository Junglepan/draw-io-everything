"""Render local PlantUML sequence examples with a verified, pinned runtime.

Requires Java 21, fontconfig and Noto Sans CJK SC; no Python packages.
Syntax checks and fresh PNG/SVG outputs are evidence of rendering, not visual review.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.request import urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'scripts' / 'plantuml-runtime.json'


def digest(path, algorithm='sha256'):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, algorithm).hexdigest()


def ensure_jar(cache, runtime):
    cache.mkdir(parents=True, exist_ok=True)
    jar = cache / f"plantuml-{runtime['version']}.jar"
    if jar.exists():
        if digest(jar, 'sha512') != runtime['sha512']:
            raise ValueError(f'Cached JAR checksum mismatch; remove and reinstall: {jar}')
        return jar
    with tempfile.TemporaryDirectory(dir=cache) as temporary:
        download = Path(temporary) / 'plantuml.jar'
        with urlopen(runtime['url'], timeout=120) as response, download.open('wb') as out:
            while block := response.read(1024 * 1024):
                out.write(block)
        if digest(download, 'sha512') != runtime['sha512']:
            raise ValueError('Downloaded JAR checksum mismatch; artifact was not installed')
        os.replace(download, jar)
    return jar


def command(args, stderr=subprocess.STDOUT):
    result = subprocess.run(args, text=True, encoding='utf-8', errors='replace',
                            stdout=subprocess.PIPE, stderr=stderr, timeout=120)
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}): {args[0]}\n{result.stdout}{result.stderr or ""}')
    return result.stdout.strip()


def check_environment(runtime):
    java = command(['java', '-version'])
    match = re.search(r'version "(\d+)', java)
    if not match or int(match[1]) != runtime['java_major']:
        raise ValueError(f"Use Java {runtime['java_major']}; found: {java}")
    font = command(['fc-match', '-f', '%{family}\n', runtime['font_family']], stderr=subprocess.PIPE)
    if not font or runtime['font_family'] not in font.splitlines()[0].split(','):
        raise ValueError(f"Install {runtime['font_family']}; fontconfig resolved: {font}")
    font_file = Path(command(['fc-match', '-f', '%{file}', runtime['font_family']], stderr=subprocess.PIPE))
    return {'java': java, 'font_family': font, 'font_file': str(font_file),
            'font_sha256': digest(font_file)}


def dependency_hashes(sources):
    """Track the examples' static, local includes; reject unresolved dependencies."""
    dependencies = {}
    pending = list(sources)
    visited = set()
    while pending:
        source = pending.pop()
        if source in visited:
            continue
        visited.add(source)
        for line in source.read_text(encoding='utf-8').splitlines():
            if not line.strip().startswith('!include'):
                continue
            match = re.fullmatch(r'\s*!include\s+([^\s]+)\s*', line)
            if not match:
                raise ValueError(f'Only static local !include is supported: {source}: {line}')
            include = (source.parent / match[1]).resolve()
            name = str(include.relative_to(ROOT))
            dependencies[name] = digest(include)
            pending.append(include)
    return dependencies


def render(sources, output, cache):
    runtime = json.loads(LOCK.read_text())
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault('XDG_CACHE_HOME', str(cache.parent))
    environment = check_environment(runtime)
    jar = ensure_jar(cache, runtime)
    java = ['java', '-Djava.awt.headless=true', '-Dfile.encoding=UTF-8', '-jar', str(jar)]
    version = command([*java, '--version'])
    if f"PlantUML version {runtime['version']} " not in version:
        raise ValueError('PlantUML version does not match the runtime lock')
    if not sources:
        return {'plantuml_version': runtime['version'], **environment}
    if len({p.stem for p in sources}) != len(sources):
        raise ValueError('Source basenames must be unique in the output directory')
    for source in sources:
        source.relative_to(ROOT)
        if not source.is_file() or source.suffix != '.puml':
            raise ValueError(f'Expected a local .puml source: {source}')
    dependencies = dependency_hashes(sources)
    source_hashes = {source: digest(source) for source in sources}
    command([*java, '-charset', 'UTF-8', '--check-syntax', *map(str, sources)])
    output.mkdir(parents=True, exist_ok=True)
    records = []
    # Stage both formats before replacing any preview; syntax-error images are not previews.
    with tempfile.TemporaryDirectory(prefix='plantuml-', dir=output) as temporary:
        stage = Path(temporary)
        for format_name in ('png', 'svg'):
            command([*java, '-charset', 'UTF-8', '--check-before-run', '--no-error-image',
                     '--format', format_name, '--output-dir', str(stage), *map(str, sources)])
        for source in sources:
            artifacts = {}
            for extension in ('png', 'svg'):
                artifact = stage / f'{source.stem}.{extension}'
                if not artifact.is_file():
                    raise ValueError(f'Renderer produced no {extension} for {source}')
                if extension == 'png':
                    if artifact.read_bytes()[:8] != b'\x89PNG\r\n\x1a\n':
                        raise ValueError(f'Invalid PNG: {artifact}')
                elif ET.parse(artifact).getroot().tag != '{http://www.w3.org/2000/svg}svg':
                    raise ValueError(f'Invalid SVG: {artifact}')
                artifacts[extension] = {'path': artifact.name, 'sha256': digest(artifact)}
            records.append({'source': str(source.relative_to(ROOT)),
                            'source_sha256': source_hashes[source], 'artifacts': artifacts})
        if dependencies != dependency_hashes(sources) or any(
                digest(source) != checksum for source, checksum in source_hashes.items()):
            raise ValueError('Sources or styles changed during rendering; rerun on the final version')
        manifest = {
            'plantuml_version': runtime['version'], 'jar_sha512': runtime['sha512'],
            'runtime_lock_sha256': digest(LOCK), 'environment': environment,
            'dependencies': dependencies,
            'cases': records,
            'checks': {'syntax': 'passed', 'png_svg_export': 'passed',
                       'semantic_review': 'not_run', 'visual_review': 'not_run'},
        }
        (stage / 'render-manifest.json').write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        for artifact in stage.iterdir():
            if artifact.name == 'render-manifest.json':
                continue
            os.replace(artifact, output / artifact.name)
        os.replace(stage / 'render-manifest.json', output / 'render-manifest.json')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sources', nargs='*', type=Path,
                        help='Local sources inside this checkout; defaults to examples/sequence/*.puml')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'examples/sequence/rendered')
    parser.add_argument('--cache-dir', type=Path, default=ROOT / '.cache/plantuml')
    parser.add_argument('--install-only', action='store_true')
    args = parser.parse_args()
    sources = [] if args.install_only else args.sources or sorted((ROOT / 'examples/sequence').glob('*.puml'))
    if not args.install_only and not sources:
        parser.error('No .puml sources selected')
    try:
        report = render([p.resolve() for p in sources], args.output_dir.resolve(), args.cache_dir.resolve())
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    if args.install_only:
        print(f"Ready: PlantUML {report['plantuml_version']}, Java 21, Noto Sans CJK SC")
    else:
        print(f"PASS: {len(report['cases'])} sources, fresh PNG + SVG; PlantUML {report['plantuml_version']}")
        print('Semantic and visual review remain separate checks.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
