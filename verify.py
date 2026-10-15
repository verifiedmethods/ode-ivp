"""Check your work for this unit and write a verification report.

Run it from a terminal in this folder:

    python verify.py

The report is written to report/verification-report.html; open it in any
web browser. You do not need to edit this file.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vm.runner import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
