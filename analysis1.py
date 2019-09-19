'''
Analyzer

Marty Jiffar
'''

'''
Checks if the sample really does have at least 50% triplets
with the same mass
'''

import experiment_preparer

def mass_checker(sample):
    same_mass = 0
    for triplet in sample:
        if triplet[0][3] == triplet[1][3] == triplet[2][3]:
            same_mass += 1

    return same_mass


if __name__ == '__main__':
    sample = experiment_preparer.experiment(50,500,30)
    mass_checker(sample)