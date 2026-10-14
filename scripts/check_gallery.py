"""Check source invariants and local documentation links (not visual semantics)."""
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as E

root=Path(__file__).resolve().parents[1]
files=sorted((root/'examples').rglob('*.drawio'))
assert len(files)==15, 'Expected 11 basic and 4 advanced gallery diagrams'
for p in files:
    tree=E.parse(p)
    cells=tree.findall('.//mxCell')
    ids=[c.attrib['id'] for c in cells]
    assert len(ids)==len(set(ids)), f'{p}: duplicate cell IDs'
    for c in cells:
        for key in ['parent','source','target']:
            if key in c.attrib: assert c.attrib[key] in ids, f'{p}: dangling {key}'
        if c.get('vertex')=='1':
            g=c.find('mxGeometry'); assert g is not None
            assert float(g.get('width','0'))>0 and float(g.get('height','0'))>0
        if c.get('edge')=='1':
            g=c.find('mxGeometry'); assert g is not None
            assert (c.get('source') and c.get('target')) or len(g.findall('mxPoint'))==2
    png=p.with_suffix('.png').read_bytes()
    assert png[:8]==b'\x89PNG\r\n\x1a\n', f'{p}: invalid PNG'
    w,h=struct.unpack('>II',png[16:24]); assert w>=1120 and h>=700
for p in [root/'README.md',root/'SKILL.md',*list((root/'references').glob('*.md'))]:
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if not link.startswith(('http:','https:','#')):
            assert (p.parent/link.split('#')[0]).exists(), f'{p}: missing {link}'
print(f'PASS: {len(files)} XML files, IDs, parent/edge references, geometry, PNG headers/dimensions and local Markdown links.')
