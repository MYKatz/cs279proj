"""
Program for bulk testing FEATURE models with different parameters.
"""

import os

FEATURE_PATH = os.getenv("FEATURE_PATH") or "./feature"

FEATURIZE = f"{FEATURE_PATH}/bin/featurize"
BUILDMODEL = f"{FEATURE_PATH}/bin/buildmodel"
SCOREIT = f"{FEATURE_PATH}/bin/scoreit"

# Parameters to test
NUM_SHELLS = [6]
SHELL_WIDTH = [1.25]
NUM_BINS = [5]