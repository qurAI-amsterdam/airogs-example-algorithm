from typing import Dict

import SimpleITK
import tqdm
import json
from pathlib import Path
import tifffile
import numpy as np

from evalutils import ClassificationAlgorithm
from evalutils.validators import (
    UniquePathIndicesValidator,
    UniqueImagesValidator,
)
from evalutils.io import ImageLoader


class DummyLoader(ImageLoader):
    @staticmethod
    def load_image(fname):
        return str(fname)


    @staticmethod
    def hash_image(image):
        return hash(image)


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

        self._file_loaders = dict(input_image=DummyLoader())

        self.output_keys = ["referable-glaucoma-likelihood", 
                            "referable-glaucoma-binary",
                            "ungradability-score",
                            "ungradability-binary"]
    
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

        pass
    
    def combine_dicts(self, dicts):
        out = {}
        for d in dicts:
            for k, v in d.items():
                if k not in out:
                    out[k] = []
                out[k].append(v)
        return out
    
    def process_case(self, *, idx, case):
        # Load and test the image for this case
        # input_image, input_image_file_path = self._load_input_image(case=case)
        if case.path.suffix == '.tiff':
            results = []
            with tifffile.TiffFile(case.path) as stack:
                for page in tqdm.tqdm(stack.pages):
                    input_image_array = page.asarray()
                    results.append(self.predict(input_image_array=input_image_array))
        else:
            input_image = SimpleITK.ReadImage(str(case.path))
            input_image_array = SimpleITK.GetArrayFromImage(input_image)

            # Classify input_image image
            results = [self.predict(input_image_array=input_image_array)]
        
        results = self.combine_dicts(results)

        # Test classification output
        if not isinstance(results, dict):
            raise ValueError("Expected a dictionary as output")

        return results

    def predict(self, *, input_image_array: np.ndarray) -> Dict:
        # From here, use the input_image to predict the output
        # We are using a not-so-smart algorithm to predict the output, you'll want to do your model inference here

        # Replace starting here
        rg_likelihood = ((input_image_array - input_image_array.min()) / (input_image_array.max() - input_image_array.min())).mean()
        rg_binary = bool(rg_likelihood > .2)
        ungradability_score = rg_likelihood * 15
        ungradability_binary = bool(rg_likelihood < .2)
        # to here with your inference algorithm

        out = {
            "referable-glaucoma-likelihood": rg_likelihood,
            "referable-glaucoma-binary": rg_binary,
            "ungradability-score": ungradability_score,
            "ungradability-binary": ungradability_binary
        }

        return out

    def save(self):
        for key in self.output_keys:
            with open(f"/output/{key}.json", "w") as f:
                out = []
                for case_result in self._case_results:
                    out += case_result[key]
                json.dump(out, f)


if __name__ == "__main__":
    airogs_algorithm().process()
