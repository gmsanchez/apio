#!venv/bin/python
"""Run apio for debugging"""

# ---------------------------------------------------
# -- Run apio for debugging by apio developers.
# -- It is not part of apio and is not installed.
# ---------------------------------------------------

# Apio developers, you can run it directly from
# command line or via Visual Studio Code debug
# targets at .vscode/launch.json.

import sys

# -- Import the apio entry point
from apio.__main__ import cli as apio

try:
    apio(None)

except SystemExit as e:
    print(f"Apio exit code: {e.code}")
