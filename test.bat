call .\build.bat

docker volume create airogs_algorithm-output

docker run --rm^
 --network none^
 --memory=15g^
 --memory-swap=15g^
 --cap-drop=ALL^
 --security-opt="no-new-privileges"^
 --shm-size=128m^
 --pids-limit=256^
 -v %~dp0\test\:/input/^
 -v airogs_algorithm-output:/output/^
 airogs_algorithm

docker run --rm^
 --network none^
 --memory=15g^
 --memory-swap=15g^
 --cap-drop=ALL^
 --security-opt="no-new-privileges"^
 --shm-size=128m^
 --pids-limit=256^
 -v airogs_algorithm-output:/output/^
 python:3.7-slim cat /output/multiple-referable-glaucoma-likelihood.json /output/multiple-referable-glaucoma-binary.json /output/multiple-ungradability-score.json /output/multiple-ungradability-binary.json

docker run --rm^
 --network none^
 --memory=15g^
 --memory-swap=15g^
 --cap-drop=ALL^
 --security-opt="no-new-privileges"^
 --shm-size=128m^
 --pids-limit=256^
 -v airogs_algorithm-output:/output/^
 -v %~dp0\test\:/input/^
 python:3.7-slim python -c "import json, sys; referable_glaucoma_likelihood = json.load(open('/output/multiple-referable-glaucoma-likelihoods.json')); referable_glaucoma_binary = json.load(open('/output/multiple-referable-glaucoma-binary.json')); ungradability_score = json.load(open('/output/multiple-ungradability-scores.json')); ungradability_binary = json.load(open('/output/multiple-ungradability-binary.json')); exp_referable_glaucoma_likelihood = json.load(open('/input/expected-multiple-referable-glaucoma-likelihoods.json')); exp_referable_glaucoma_binary = json.load(open('/input/expected-multiple-referable-glaucoma-binary.json')); exp_ungradability_score = json.load(open('/input/expected-multiple-ungradability-scores.json')); exp_ungradability_binary = json.load(open('/input/expected-multiple-ungradability-binary.json')); sys.exit((referable_glaucoma_likelihood != exp_referable_glaucoma_likelihood) | (referable_glaucoma_binary != exp_referable_glaucoma_binary) | (ungradability_score != exp_ungradability_score) | (ungradability_binary != exp_ungradability_binary))"

if %ERRORLEVEL% == 0 (
	echo "Tests successfully passed..."
)
else
(
	echo "Expected output was not found..."
)

docker volume rm airogs_algorithm-output
