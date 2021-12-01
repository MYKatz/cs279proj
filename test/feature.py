"""
Program for bulk testing FEATURE models with different parameters.
"""

import os
import tempfile

FEATURE_PATH = os.getenv("FEATURE_PATH") or "./feature"

FEATURIZE = f"{FEATURE_PATH}/bin/featurize"
BUILDMODEL = f"{FEATURE_PATH}/bin/buildmodel"
SCOREIT = f"{FEATURE_PATH}/bin/scoreit"

# Training examples paths
POSITIVE_TRAINING_EXAMPLES = "/home/katz/Code/cs279proj/example/trypsin_ser_og.pos.ptf"
NEGATIVE_TRAINING_EXAMPLES = "/home/katz/Code/cs279proj/example/trypsin_ser_og.neg.ptf"

# Parameters to test
NUM_SHELLS = [6]
SHELL_WIDTH = [1.25]
NUM_BINS = [5]


def build_feature_model(num_shells, shell_width, num_bins):

    out_dir = f"out/{num_shells}-{shell_width}-{num_bins}"
    os.makedirs(out_dir)

    os.system(
        f"{FEATURIZE} -n {num_shells} -w {shell_width} -P {POSITIVE_TRAINING_EXAMPLES} > {out_dir}/pos.ff"
    )
    os.system(
        f"{FEATURIZE} -n {num_shells} -w {shell_width} -P {NEGATIVE_TRAINING_EXAMPLES} > {out_dir}/neg.ff"
    )

    os.system(
        f"{BUILDMODEL} -n {num_shells} -b {num_bins} {out_dir}/pos.ff {out_dir}/neg.ff > {out_dir}/model.model"
    )

    return f"{out_dir}/model.model"


for num_shells in NUM_SHELLS:
    for shell_width in SHELL_WIDTH:
        for num_bins in NUM_BINS:
            # relative model path
            model_path = build_feature_model(num_shells, shell_width, num_bins)