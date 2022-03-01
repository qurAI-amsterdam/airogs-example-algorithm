# AIROGS Example Algorithm

This is an example repository for how to make an algorithm submission for the [AIROGS challenge](https://airogs.grand-challenge.org). This algorithm is just for inference of your model.

You can upload your algorithms [here](https://grand-challenge.org/algorithms/create/). If you have a verfied account on Grand Challenge and are accepted as a participant in the AIROGS challenge, you should be able to submit your Docker container. If something does not work for you, please do not hesitate to [contact us](mailto:c.w.devente@uva.nl) or [add a post in the forum](https://grand-challenge.org/forums/forum/airogs-609/). If the problem is related to the code of this repository, please create a new issue on GitHub.

Here are some links that may also be useful:
- [Tutorial on how to make an algorithm container on Grand Challenge](https://grand-challenge.org/blogs/create-an-algorithm/)
- [Docker documentation](https://docs.docker.com/)
- [Evalutils documentation](https://evalutils.readthedocs.io/)
- [Grand Challenge documentation](https://comic.github.io/grand-challenge.org/algorithms.html)

## Prerequisites

You will need to have [Docker](https://docs.docker.com/) installed on your system. We recommend to use [WSL 2.0](https://docs.microsoft.com/en-us/windows/wsl/install) if you are on Windows or to use Linux and install Docker there.

## Adapt the container to your algorithm

This codebase uses a not-so-smart algorithm that you may want to adapt to a smarter one that was training using the training data provided on the challenge web page. This section explains how to do that.

1. Change the `Dockerfile`.

    a. You may want to change `FROM python:3.7-slim` to another base image that already has some machine learning packages installed, such as `FROM pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime`.

    b. Install the required packages, see comment in `Dockerfile` for an example.

    c. Copy additional files, such as model weights, see comment in `Dockerfile` for example.

2. All the magic happens in `process.py`, specifically in the `predict` function of the `airogs_algorithm` class in that file. This function reads a single image, processes it and outputs a dictionary with the four expected outputs. Replace the dummy code in this function with the code for your inference algorihm. You may also want to load your model weights etc. in the `__init__` function and use them later in the `predict` function.

3. Run `test.sh` (or `test.bat` if you are on Windows and not on WSL 2.0) to build the container. This will also build the container. The output of this script should end like this (probably with different values for the four model outputs):
    ```
    airogs_algorithm-output
    100%|██████████| 10/10 [00:01<00:00,  8.29it/s]
    [0.2747808088700938, 0.1968278557040863, 0.3251099105817551, 0.251309593349525, 0.16331946039347478, 0.09951439097624658, 0.1523684949346395, 0.14107948132725376, 0.16315452661077018, 0.1829633503171027][true, false, true, true, false, false, false, false, false, false][4.121712133051407, 2.952417835561295, 4.876648658726326, 3.769643900242875, 2.4497919059021216, 1.4927158646436987, 2.2855274240195924, 2.1161922199088066, 2.4473178991615527, 2.7444502547565404][false, true, false, false, true, true, true, true, true, true]
    Tests successfully passed...
    ```

4. Run `export.sh`, which will produce `airogs_algorithm.tar.gz`. We will need this file later when uploading the algorithm to Grand Challenge.

5. Make a new algorithm [here](https://grand-challenge.org/algorithms/create/). Fill in the fields as specified on the form. Some important fields are:

    a. `Viewer`: Choose `Viewer CIRRUS Core (Public)`.
    
    b. `Inputs`: Choose `Color Fundus Image (Image)`.

    c. `Outputs`: Choose `Multiple Referable Glaucoma Likelihood (Anything)`, `Multiple Referable Glaucoma Binary Decisions (Anything)`, `Multiple Ungradability Scores (Anything)`, `Multiple Ungradability Binary Decisions (Anything)`.

    When you are done, click `Save`.

6. On the page of your new algorithm, go to `Containers` in the menu on the left and click `Upload a Container`. Now upload your `.tar.gz` file produced in step 4. You could also not build the container yourself, but use a GitHub repo. Then you should click `Link GitHub Repo` instead. It will take some time before your Docker container is `Ready`. Do not proceed with the following steps, once this is the case.

7. You can try out your own algorithm when clicking `Try-out Algorithm` on the page of your algorithm, again in the left menu.

8. Now, we will make a submission to one of the test phases. Go to the [AIROGS Challenge page](https://airogs.grand-challenge.org/) and click `Submit`. Choose which phase you want to submit to and fill out the form. Under `Algorithm`, you choose the algorithm that you just created. Then hit `Save`. After the processing in the backend is done, your submission should pop up on the leaderboard.
