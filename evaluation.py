import math
import os
import json
import h5py

from connectomics.utils.evaluate import adapted_rand
from evalutils.evalutils import (
    DEFAULT_INPUT_PATH,
    DEFAULT_EVALUATION_OUTPUT_FILE_PATH,
    DEFAULT_GROUND_TRUTH_PATH,
)


class Snemi3d:
    def __init__(self):
        self.input_file = os.path.join(DEFAULT_INPUT_PATH, "test-input.h5")
        self.output_file = DEFAULT_EVALUATION_OUTPUT_FILE_PATH
        self.gt_file = os.path.join(DEFAULT_GROUND_TRUTH_PATH, "test-labels.h5")

        self.slice_to_third = True

    def load(self):
        with h5py.File(self.input_file, "r") as f:
            self.input = f["main"][()]
        with h5py.File(self.gt_file, "r") as f:
            self.ground_truth = f["main"][()]
        if self.slice_to_third:
            self.slice()

    def evaluate(self):
        self.load()

        metrics = {"adapted_rand_error": adapted_rand(self.input, self.ground_truth)}

        with open(self.output_file, "w") as f:
            f.write(json.dumps(metrics))

    def slice(self):
        # only use a third of the number of voxels
        z, y, x = self.ground_truth.shape
        n_voxels = z * y * x
        new_z = z / 2
        new_x = new_y = int(math.sqrt(n_voxels * 0.33 / new_z))
        z0 = new_z // 2
        z1 = new_z / 2 + new_z
        y0 = y // 2 - new_y // 2
        y1 = y0 + new_y
        x0 = x // 2 - new_x // 2
        x1 = x0 + new_x

        z0, z1, y0, y1, x0, x1 = map(int, [z0, z1, y0, y1, x0, x1])

        self.input = self.input[z0:z1, y0:y1, x0:x1]
        self.ground_truth = self.ground_truth[z0:z1, y0:y1, x0:x1]


if __name__ == "__main__":
    Snemi3d().evaluate()
