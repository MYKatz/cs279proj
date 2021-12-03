"""
Program for bulk testing FEATURE models with different parameters.
"""

import os
import time
import tempfile

FEATURE_PATH = os.getenv("FEATURE_PATH") or "./feature"

FEATURIZE = f"{FEATURE_PATH}/bin/featurize"
BUILDMODEL = f"{FEATURE_PATH}/bin/buildmodel"
SCOREIT = f"{FEATURE_PATH}/bin/scoreit"

# Training examples paths
POSITIVE_TRAINING_EXAMPLES = "/home/katz/Code/cs279proj/example/trypsin_ser_og.pos.ptf"
NEGATIVE_TRAINING_EXAMPLES = "/home/katz/Code/cs279proj/example/trypsin_ser_og.neg.ptf"

EVAL_EXAMPLES = "/home/katz/Code/cs279proj/eval/"
EVAL_NAME = "1bqy_ser_og" # .ff file should exist, will create .ptf

GAUSSIAN_LABEL="gauss"

# Parameters to test
NUM_SHELLS = [
    6,
    3,
]
SHELL_WIDTH = [1.25, 1, 0.5]
NUM_BINS = [5, 10]

def build_feature_model(num_shells, shell_width, num_bins):

    start_time = time.time()

    out_dir = f"out/{num_shells}-{shell_width}-{num_bins}-{GAUSSIAN_LABEL}"
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

    model_build_time = time.time() - start_time

    os.system(f"echo {model_build_time} > {out_dir}/model_build_time")

    return f"{out_dir}/model.model"


def score_model(model_path, num_shells, shell_width):

    start_time = time.time()

    out_dir = model_path.replace("/model.model", "")

    # regenerate .ff file
    os.system(f"rm {EVAL_EXAMPLES}/{EVAL_NAME}.ff")
    os.system(f"{FEATURIZE} -n {num_shells} -w {shell_width} -P {EVAL_EXAMPLES}/{EVAL_NAME}.ptf > {EVAL_EXAMPLES}/{EVAL_NAME}.ff")

    os.system(f"{SCOREIT} -a {model_path} {EVAL_EXAMPLES}/{EVAL_NAME}.ff > {out_dir}/hits.hits")
    # remove comments
    os.system(f"sed '/^#/d' {out_dir}/hits.hits > {out_dir}/hits_cleaned.hits")
    os.system(f"sort -k2 -n {out_dir}/hits_cleaned.hits > {out_dir}/hits.sorted")

    eval_time = time.time() - start_time

    os.system(f"echo {eval_time} > {out_dir}/eval_time")


for num_shells in NUM_SHELLS:
    for shell_width in SHELL_WIDTH:
        for num_bins in NUM_BINS:
            # relative model path
            model_path = build_feature_model(num_shells, shell_width, num_bins)
            score_model(model_path, num_shells, shell_width)