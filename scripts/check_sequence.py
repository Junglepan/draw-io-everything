"""Check current PlantUML outputs and their evidence, not arbitrary UML correctness."""
import argparse
import json
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET

from render_sequence import dependency_hashes, digest, LOCK, ROOT

EXPECTED = {
    'reservation': ['预约用户', '预约入口', '预约服务', '预约存储', '请求有效', '请求无效', '容量不足', '参数错误'],
    'reservation-long-labels': ['团队会议室', '预约申请人', '企业协同平台', '记录与容量存储', '返回可用容量不足提示'],
    'reservation-extra-participant': ['权限服务', '检查预约权限', '允许预约', '拒绝预约', '无权限'],
    'reservation-branches': ['已有预约', '返回原预约编号', '未命中', '幂等键唯一约束'],
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(output):
    manifest = json.loads((output / 'render-manifest.json').read_text())
    runtime = json.loads(LOCK.read_text())
    require(manifest['runtime_lock_sha256'] == digest(LOCK), 'Runtime lock changed; rerender')
    require(manifest['plantuml_version'] == runtime['version'], 'Wrong PlantUML version')
    require(manifest['jar_sha512'] == runtime['sha512'], 'Wrong renderer checksum')
    for name, checksum in manifest['dependencies'].items():
        require(digest(ROOT / name) == checksum, f'Style changed; rerender: {name}')
    cases = manifest['cases']
    require(len(cases) == len(EXPECTED), 'Expected four rendered cases, not an empty or partial run')
    require({Path(c['source']).stem for c in cases} == set(EXPECTED), 'Wrong selected cases')
    require(manifest['dependencies'] == dependency_hashes([ROOT / c['source'] for c in cases]),
            'Local include dependencies changed or are missing; rerender')
    for case in cases:
        source = ROOT / case['source']
        require(digest(source) == case['source_sha256'], f'Source changed; rerender: {source}')
        for extension in ('png', 'svg'):
            artifact = case['artifacts'][extension]
            path = output / artifact['path']
            require(digest(path) == artifact['sha256'], f'Preview hash mismatch: {path}')
        png = (output / case['artifacts']['png']['path']).read_bytes()
        require(png[:8] == b'\x89PNG\r\n\x1a\n', f'Invalid PNG for {source}')
        width, height = struct.unpack('>II', png[16:24])
        require(width > 0 and height > 0, f'Empty preview for {source}')
        svg = ET.parse(output / case['artifacts']['svg']['path']).getroot()
        require(svg.tag == '{http://www.w3.org/2000/svg}svg', f'Invalid SVG for {source}')
        text = '\n'.join(''.join(e.itertext()) for e in svg.iter('{http://www.w3.org/2000/svg}text'))
        for label in EXPECTED[source.stem]:
            require(label in text, f'Expected label missing from rendered SVG: {source}: {label}')
    require(manifest['checks']['syntax'] == 'passed', 'Syntax check did not pass')
    require(manifest['checks']['png_svg_export'] == 'passed', 'Export did not pass')
    return len(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'examples/sequence/rendered')
    args = parser.parse_args()
    try:
        count = check(args.output_dir)
    except (OSError, ValueError, KeyError, ET.ParseError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 1
    print(f'PASS: {count} cases, source/style/runtime/preview hashes, PNG + SVG and expected labels')
    print('This does not replace semantic and visual review.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
