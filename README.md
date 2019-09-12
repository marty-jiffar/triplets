# Cloth Perception Experiment


The experimental design is as follows:

Using the parameters of stiffness (6 levels), mass (7 levels), texture (7 levels), and scene/wind (3 types), we generated 882 videos -- using all possible permutations of the parameters.

We will show the participant 3 videos per trial: an anchor video, a positive video with the same stiffness as the anchor, and a negative video with a different stiffness. Their task is to identify the negative.

From all the possible triplets, sampling.py takes a random sample of size k (500 for preliminary testing, later probably 5000).

The program also accepts another parameter to determine the 'hardness' of the sample. Each randomly sampled triplet is assigned a hardness score based on how difficult it is to determine the negative. For example: if the negative is 5 stiffness levels away from the positive and anchor, it is much easier to tell than if the negative is only 1 stiffness level away from the other two. It is also easier to differentiate the negative if all of the videos have a different scene, rather than if the negative shares a scene with the anchor and not with the positive, or with the positive and not the anchor.

experiment_preparer.py runs sampling.py, breaks up the output into blocks (to save data periodically), and saves those blocks as individual CSV and JSON files. Each line in the CSV/JSON files contains the triplet index, the three file names for the anchor, positive, and negative, and the triplet's hardness score.

The web_display folder has the HTML, JavaScript, and CSS files that create an interface for the participant to actually complete the experiment, as well as a PHP file that stores their data.
