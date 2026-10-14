"""Rebuild the eleven scenario examples (XML only)."""
import runpy
from pathlib import Path

if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    for name in ['build_gallery_process.py', 'build_gallery_systems.py']:
        runpy.run_path(str(here / name), run_name='__main__')
