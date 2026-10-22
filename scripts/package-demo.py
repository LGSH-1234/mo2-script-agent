"""Build a source + prebuilt web distribution, never including local credentials/data."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import sys

root = Path(__file__).resolve().parents[1]
output = Path(sys.argv[1]).resolve()
output.parent.mkdir(parents=True, exist_ok=True)
excluded = {'.git', '.venv', 'node_modules', 'local-data', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.DS_Store'}
files = []
for path in root.rglob('*'):
    rel = path.relative_to(root)
    if not path.is_file() or path.is_symlink() or excluded.intersection(rel.parts):
        continue
    if path.name.startswith('.env') and path.name != '.env.example':
        continue
    if path.suffix in {'.pyc', '.sqlite', '.sqlite3', '.db', '.log', '.zip'} or rel.parts[:2] == ('docs', 'feishu'):
        continue
    files.append((path, rel))
with ZipFile(output, 'w', ZIP_DEFLATED) as package:
    for path, rel in files:
        package.write(path, Path('mo2-script-agent') / rel)
with ZipFile(output) as package:
    assert package.testzip() is None
    assert not any(excluded.intersection(Path(n).parts) or Path(n).name == '.env' for n in package.namelist())
print(f'{output.name}: {len(files)} files, {output.stat().st_size / 1024 / 1024:.1f} MB; archive verified; credentials and local data excluded.')
