# CS279 project - FEATURE testing

## Run steps:

1. Download feature source code.
2. Set OS env var `PDB_DIR` to folder path of pdbs and `FEATURE_DIR` to feature/data, `DSSP_DIR` etc
3. Set OS env var `FEATURE_PATH` to feature source code folder path
4. Add the `.../feature/tools/lib` directory to PYTHONPATH (ie run "export PYTHONPATH="${PYTHONPATH}:/path/to/feature/tools/lib")
5. Write the rest of the code
6. Run

## Configuration

Set `USE_GAUSSIAN` const in NaiveBayesClassifier.cc and Model.cc if you want to sample from a gaussian rather than unifrom distribution in the Naive bayes training process. Remember to recompile feature (yes, this is a dumb way to do this. sue me.)


