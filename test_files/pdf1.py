import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

pdf1 = open("AAPL.pdf", "r")
print(pdf1.read())