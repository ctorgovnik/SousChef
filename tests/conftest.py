import os
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent  # Goes up one level from tests/
sys.path.append(str(src_path)) 