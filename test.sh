#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

./build.sh

docker volume create airogs_algorithm-output

docker run --rm \
        --memory=15g \
        -v $SCRIPTPATH/test/:/input \
        -v airogs_algorithm-output:/output/ \
        airogs_algorithm

docker run --rm \
        -v airogs_algorithm-output:/output/ \
        python:3.7-slim cat /output/referable-glaucoma-likelihood.json /output/referable-glaucoma-binary.json /output/ungradability-score.json /output/ungradability-binary.json

docker run --rm \
        -v airogs_algorithm-output:/output/ \
        -v $SCRIPTPATH/test/:/input \
        python:3.7-slim python -c """import json, sys
referable_glaucoma_likelihood = json.load(open('/output/referable-glaucoma-likelihood.json'))
referable_glaucoma_binary = json.load(open('/output/referable-glaucoma-binary.json'))
ungradability_score = json.load(open('/output/ungradability-score.json'))
ungradability_binary = json.load(open('/output/ungradability-binary.json'))

exp_referable_glaucoma_likelihood = json.load(open('/input/expected-referable-glaucoma-likelihood.json'))
exp_referable_glaucoma_binary = json.load(open('/input/expected-referable-glaucoma-binary.json'))
exp_ungradability_score = json.load(open('/input/expected-ungradability-score.json'))
exp_ungradability_binary = json.load(open('/input/expected-ungradability-binary.json'))

sys.exit((referable_glaucoma_likelihood != exp_referable_glaucoma_likelihood) |
(referable_glaucoma_binary != exp_referable_glaucoma_binary) |
(ungradability_score != exp_ungradability_score) |
(ungradability_binary != exp_ungradability_binary))"""

if [ $? -eq 0 ]; then
    echo "Tests successfully passed..."
else
    echo "Expected output was not found..."
fi

docker volume rm airogs_algorithm-output
