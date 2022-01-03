from typing import Dict

import SimpleITK
import random
import json
from pathlib import Path

from evalutils import ClassificationAlgorithm
from evalutils.validators import (
    UniquePathIndicesValidator,
    UniqueImagesValidator,
)


class airogs_algorithm(ClassificationAlgorithm):
    def __init__(self):
        super().__init__(
            validators=dict(
                input_image=(
                    UniqueImagesValidator(),
                    UniquePathIndicesValidator(),
                )
            ),
        )

        self.output_keys = ["referable-glaucoma-likelihood", "referable-glaucoma-binary", "ungradability-score", "ungradability-binary"]
    
    def load(self):
        for key, file_loader in self._file_loaders.items():
            fltr = (
                self._file_filters[key] if key in self._file_filters else None
            )
            self._cases[key] = self._load_cases(
                folder=Path("/input/images/color-fundus/"),
                file_loader=file_loader,
                file_filter=fltr,
            )
    
    def process_case(self, *, idx, case):
        # Load and test the image for this case
        input_image, input_image_file_path = self._load_input_image(case=case)

        # Classify input_image image
        results = self.predict(input_image=input_image)

        # Test classification output
        if not isinstance(results, dict):
            raise ValueError("Expected a dictionary as output")

        return results

    def predict(self, *, input_image: SimpleITK.Image) -> Dict:
        # From here, use the input_image to predict the output
        input_image_array = SimpleITK.GetArrayFromImage(input_image)

        # We are using a not very smart algorithm to predict the output, you probably want to do your model inference here

        # Replace starting here
        rg_likelihood = ((input_image_array - input_image_array.min()) / (input_image_array.max() - input_image_array.min())).mean()
        rg_binary = bool(rg_likelihood > .2)
        ungradability_score = rg_likelihood * 15
        ungradability_binary = bool(rg_likelihood < .2)
        # to here with your inference algorithm

        out = {
            "referable-glaucoma-likelihood": rg_likelihood,  # Likelihood for 'referable glaucoma'
            "referable-glaucoma-binary": rg_binary,  # True if 'referable glaucoma', False if 'no referable glaucoma'
            "ungradability-score": ungradability_score,  # True if 'ungradable', False if 'gradable'
            "ungradability-binary": ungradability_binary  # The higher the value, the more likely the label is 'ungradable'
        }

        return out

    def save(self):
        for key in self.output_keys:
            with open(f"/output/{key}.json", "w") as f:
                json.dump(self._case_results[0][key], f)


if __name__ == "__main__":
    airogs_algorithm().process()
