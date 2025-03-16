import sys
from pathlib import Path

# Add the src directory to the Python path so tests can import modules from src
src_path = Path(__file__).parent.parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

app_path = Path(__file__).parent.parent / "app"
if app_path.exists():
    sys.path.insert(0, str(app_path))
