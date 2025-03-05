import os
import sys
from pathlib import Path

# Add project root to Python path
root_path = Path(__file__).parent.parent  # Goes up one level from tests/
sys.path.append(str(root_path))

# Add src to Python path (if needed)
src_path = root_path / "src"
sys.path.append(str(src_path)) 