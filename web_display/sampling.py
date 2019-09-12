'''
Sampling triplets based on parameters


Marty Jiffar
'''

import random
import math
import csv
import itertools
import numpy as np
# import matplotlib.pyplot as plt
from itertools import product
from tqdm import tqdm
import hard_rating

'''
Takes random sample of triplets from all possible permutations

Inputs:
- k (int): sample size
- pct_hard (int): percentage of sample that is harder (1 - 100)

Returns:
- sample (list of triplets): triplet sample of size k
'''
def sampler(k, pct_hard):

    TEXTURE = ['Sha', 'Fleece', 'Bro', 'Sweater', 'FeltGreen',
                'Cotton', 'Silk']
    SCENES = [1, 2, 3]
    STIFFNESS = [0.001, 0.01, 0.1, 1, 10, 100]
    MASS = [0.1, 0.3, 0.5, 0.7, 1, 1.3, 1.7]

    anchor_num = len(STIFFNESS)*len(SCENES)*len(MASS)*len(TEXTURE)
    pos_num = len(SCENES)*len(MASS)*len(TEXTURE)
    neg_num = (len(STIFFNESS)-1)*len(SCENES)*len(MASS)*len(TEXTURE)

    total_num = anchor_num*pos_num*neg_num 
    sample = []
    anchor_count = 0

    sample_difficulty = []

    anchor_list = list(itertools.product(TEXTURE, SCENES, STIFFNESS, MASS))
    for anchor in tqdm(anchor_list):
        stiff = [anchor[2]]
        pos_list = list(itertools.product(TEXTURE, SCENES, stiff, MASS))
        neg_stiff = list(set(STIFFNESS) - set([anchor[2]]))
        neg_list = list(itertools.product(TEXTURE, SCENES, neg_stiff, MASS))
        triplets = list(itertools.product(pos_list, neg_list))

        # sampling algorithm inspo by http://metadatascience.com/2014/02/27/
        # random-sampling-from-very-large-files/
        smpl_from_each = math.ceil(k / anchor_num)
        random_set = sorted(random.sample(range(len(pos_list)*
                                                len(neg_list)), 
                                                smpl_from_each))
        # preferentially sample harder triplets
        for i in range(smpl_from_each):
            # compare each randomly sampled triplet to its neighbor
            current_triplet = (anchor,) + triplets[random_set[i]]
            prev_triplet = (anchor,) + triplets[random_set[i]-1]
            current_rating = hard_rating.total_rating(current_triplet)
            prev_rating = hard_rating.total_rating(prev_triplet)
            # figure out which triplet is 'harder' through rating
            if current_rating < prev_rating:
                easier_triplet = current_triplet
                harder_triplet = prev_triplet
            elif current_rating > prev_rating:
                harder_triplet = current_triplet
                easier_triplet = prev_triplet
            else: # if rating is equal, just choose current riplet
                easier_triplet = current_triplet
                harder_triplet = current_triplet
                chosen_triplet = current_triplet
            # choose harder triplet pct_hard% of the time (ex. 60%)
            if random.randint(1, 100) <= pct_hard:
                chosen_triplet = harder_triplet
            else:
                chosen_triplet = easier_triplet
            sample.append(chosen_triplet)
            sample_difficulty.append(hard_rating.total_rating(chosen_triplet))

        anchor_count += 1

    # in sampling equally from each anchor, we usually generate too many
    # samples, so this removes indices randomly
    random.shuffle(sample)
    for i in range(len(sample) - k):
        sample.pop()


    return sample

'''
def histogram(sample, pct_hard):
    sample_difficulty = []
    for i in range(len(sample)):
        sample_difficulty.append(hard_rating.total_rating(sample[i]))
    # plots histogram of difficulty scores
    samply = np.array(sample_difficulty)
    mean = round(np.mean(samply), 3)
    stdev = round(np.std(samply), 3)
    plt.hist(samply, bins = 23)
    plt.ylabel('Frequency')
    plt.xlabel('Hardness Score')
    plt.title('Distribution of Hardness for Sample'
        ' with Hard Bias of ' + str(pct_hard) + '%')
    plt.text(9, 900, r'$\mu =$')
    plt.text(10, 900, str(mean))
    plt.text(9, 850, 'sd =')
    plt.text(10, 850, str(stdev))
    plt.show()
 '''


def run():
    sample = sampler(5000, 50)
    # histogram(sample, 50)


if __name__ == "__main__":
    run()

