# CS279 project - FEATURE testing

## Run steps:

1. Download feature source code.
2. Set OS env var `PDB_DIR` to folder path of pdbs (pdbs/calcium) and `FEATURE_DIR` to feature/data, `DSSP_DIR` to folder path of DSSPs (dssp/calcium)
3. Set OS env var `FEATURE_PATH` to feature source code folder path
4. Add the `.../feature/tools/lib` directory to PYTHONPATH (ie run "export PYTHONPATH="${PYTHONPATH}:/path/to/feature/tools/lib")
5. Update constants in `test/feature.py`, `test/eval.py` to point to correct paths on local machine
6. To train models, run `test/feature.py`. To evaluate models and generate results, run `test/eval.py`

## Configuration

Set `USE_GAUSSIAN` const in NaiveBayesClassifier.cc and Model.cc if you want to sample from a gaussian rather than unifrom distribution in the Naive bayes training process. Remember to recompile feature once this change is made (yes, this is poor practice, but we were short on time :(    )

## Citations

Almost all code in the `feature` directory is FEATURE 3.1, downloaded from https://simtk.org/projects/feature. The exceptions to this are `NaiveBayesClassifier.cc` and `Model.cc`, which contain modifications that implement Gaussian Naive Bayes features. These files also contain John D Cook's normal CDF implementation, which was released into the public domain and can be originally found at https://www.johndcook.com/blog/cpp_phi/ 

All of the code in the `test` directory is ours -- this includes the test harness and evaluation script.