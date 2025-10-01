import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)  # adjust based on your structure
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
print(TEMPLATES_DIR)