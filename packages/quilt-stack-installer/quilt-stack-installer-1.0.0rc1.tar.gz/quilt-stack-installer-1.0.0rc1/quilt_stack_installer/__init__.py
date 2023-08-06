from pathlib import Path

p = Path(__file__).parent/"VERSION"
__version__ = p.read_text()
