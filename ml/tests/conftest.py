"""
Pytest configuration for PropValueAI tests.
Adds the project root directory to sys.path so modules like ml.common are discoverable.
"""

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
