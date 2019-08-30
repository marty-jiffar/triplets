'''
Sampling triplets based on parameters


Marty Jiffar
'''

import random
import math
import csv
import itertools
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from tqdm import tqdm
import hard_rating

'''
Takes random sample of triplets from all possible permutations

Inputs:
- stiff__ (int): stiffness of cloth
- scenes__ (int): scene of video
- mass__ (int)
- text__ (int): texture of cloth
- k (int): sample size
- pct_hard (int): percentage of sample that is harder (1 - 100)

Returns:
- sample (list of triplets): triplet sample of size k
'''
def sampler(stiff__, scenes__, mass__, text__, k, pct_hard):

    STIFFNESS = []
    SCENES = []
    MASS = []
    TEXTURE = []

    i = 0
    j = 0
    l = 0
    m = 0

    while i < stiff__:
        STIFFNESS.append(i)
        i += 1
    while j < scenes__:
        SCENES.append(j)
        j += 1
    while l < mass__:
        MASS.append(l)
        l += 1
    while m < text__:
        TEXTURE.append(m)
        m += 1

    anchor_num = len(STIFFNESS)*len(SCENES)*len(MASS)*len(TEXTURE)
    pos_num = len(SCENES)*len(MASS)*len(TEXTURE)
    neg_num = (len(STIFFNESS)-1)*len(SCENES)*len(MASS)*len(TEXTURE)

    total_num = anchor_num*pos_num*neg_num 
    sample = []
    anchor_count = 0

    sample_difficulty = []

    anchor_list = list(itertools.product(STIFFNESS, SCENES, MASS, TEXTURE))
  #  print("anchor len: ", len(anchor_list))
    for anchor in tqdm(anchor_list):
     #   print("anchor:", anchor)
        stiff = [anchor[0]]
   #     print("stiff: ", stiff)
        pos_list = list(itertools.product(stiff, SCENES, MASS, TEXTURE))
    #    print("pos len: ", len(pos_list))
        neg_stiff = list(set(STIFFNESS) - set([anchor[0]]))
        neg_list = list(itertools.product(neg_stiff, SCENES, MASS, TEXTURE))
    #    print("neg len: ", len(neg_list))
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

        #print("anchor_count: ", anchor_count)
        anchor_count += 1

    # in sampling equally from each anchor, we usually generate too many
    # samples, so this removes indices randomly
    random.shuffle(sample)
    for i in range(len(sample) - k):
        sample.pop()


    return sample

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


def run():
    sampler(6, 3, 7, 7, 5000, 20)
    histogram(20)


if __name__ == "__main__":
    run()

