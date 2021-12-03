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

ATOMSELECTOR_PATH = f"{FEATURE_PATH}/tools/bin/atomselector.py"

# Training examples paths
POSITIVE_TRAINING_EXAMPLES = "/home/katz/Code/cs279proj/example/t_ca_sites.ptf"
NEGATIVE_TRAINING_EXAMPLES = "/home/katz/Code/cs279proj/example/t_ca_nonsites.ptf"

EVAL_EXAMPLES = "/home/katz/Code/cs279proj/eval/"
EVAL_NAME = "eval" # .ff file should exist, will create .ptf
EVAL_IDS = [
    "1ARV",
    "1AXN",
    "1BP2",
    "1CEL",
    "1CLC",
    "1CVL",
    "1DJX",
    "1ESL",
    "1GCA",
    "1IVD",
    "1JAP",
    "1KIT",
    "1KUH",
    "1MHL",
    "1OVA",
    "1PNK",
    "1POC",
    "1RGA",
    "1SAC",
    "1SCM",
    "1SGT",
    "1SMD",
    "1SNC",
    "1SRA",
    "1TCO",
    "1TF4",
    "1TRK",
    "1WAD",
    "1XJO",
    "2AAA",
    "2AMG",
    "2AYH",
    "2MPR",
    "2POR",
    "2PRK",
    "2SCP",
    "3DNI",
    "3MIN",
    "4SBV",
    "8TLN"
]

GAUSSIAN_LABEL="gauss"

# Parameters to test
NUM_SHELLS = [
    4,
]
SHELL_WIDTH = [1.25]
NUM_BINS = [5]

def build_feature_model(num_shells, shell_width, num_bins):

    start_time = time.time()

    out_dir = f"out/{num_shells}-{shell_width}-{num_bins}-{GAUSSIAN_LABEL}-expr"
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


def generate_eval_data():
    for pdb_id in EVAL_IDS:
        os.system(f"python2.7 {ATOMSELECTOR_PATH} {pdb_id} >> {EVAL_EXAMPLES}/{EVAL_NAME}.ptf")




def score_model(model_path, num_shells, shell_width):

    start_time = time.time()

    out_dir = model_path.replace("/model.model", "")

    # regenerate .ff file
    os.system(f"rm {EVAL_EXAMPLES}/{EVAL_NAME}.ff")
    os.system(f"{FEATURIZE} -n {num_shells} -w {shell_width} -P {EVAL_EXAMPLES}/{EVAL_NAME}.ptf > {EVAL_EXAMPLES}/{EVAL_NAME}.ff")

    os.system(f"{SCOREIT} -a {model_path} {EVAL_EXAMPLES}/{EVAL_NAME}.ff > {out_dir}/hits.hits")
    # remove comments
    os.system(f"sed '/^#/d' {out_dir}/hits.hits > {out_dir}/hits_cleaned.hits")
    os.system(f"sort -r -k2 -n {out_dir}/hits_cleaned.hits > {out_dir}/hits.sorted")

    eval_time = time.time() - start_time

    os.system(f"echo {eval_time} > {out_dir}/eval_time")

if __name__ == "__main__":
    for num_shells in NUM_SHELLS:
        for shell_width in SHELL_WIDTH:
            for num_bins in NUM_BINS:
                # relative model path
                model_path = build_feature_model(num_shells, shell_width, num_bins)
                score_model(model_path, num_shells, shell_width)