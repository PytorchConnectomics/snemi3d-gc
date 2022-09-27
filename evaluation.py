import os
import json
import h5py

from connectomics.utils.evaluate import adapted_rand
from evalutils.evalutils import DEFAULT_INPUT_PATH, DEFAULT_EVALUATION_OUTPUT_FILE_PATH, DEFAULT_GROUND_TRUTH_PATH


class Snemi3d:
    def __init__(self):
        self.input_file = os.path.join(DEFAULT_INPUT_PATH, "test-input.h5")
        self.output_file = DEFAULT_EVALUATION_OUTPUT_FILE_PATH
        self.gt_file = os.path.join(DEFAULT_GROUND_TRUTH_PATH, "test-labels.h5")

    def load(self):
        with h5py.File(self.input_file, "r") as f:
            self.input = f["main"][()]
        with h5py.File(self.gt_file, "r") as f:
            self.ground_truth = f["main"][()]
    def evaluate(self):
        self.load()

        metrics = { "adapted_rand_error" : adapted_rand(self.input, self.ground_truth) }

        with open(self.output_file, "w") as f:
            f.write(json.dumps(metrics))

if __name__ == "__main__":
    Snemi3d().evaluate()
