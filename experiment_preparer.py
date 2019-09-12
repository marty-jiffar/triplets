'''
Setting up experiment: drawing sample, dividing it into blocks,
putting blocks into CSV files and converting them to JSON files
to prepare for handling in JavaScript

Marty Jiffar
'''

import csv
import json
import math
import sampling
import hard_rating

'''
Creates CSV of sample

Inputs:
- sample (list of triplets)
- name (string): name of csv file
'''
def smpl_csv(sample, name):
    with open(name, 'w') as sample_file:
        writer = csv.writer(sample_file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Triplet #', 'Anchor', 
                    'Positive', 'Negative', 'Hardness Score'])
    for i in range(len(sample)):
        with open(name, 'a') as sample_file:
            writer = csv.writer(sample_file)
            anchor = sample[i][0]
            positive = sample[i][1]
            negative = sample[i][2]
            anchor_file = (anchor[0] + '_wind' + str(anchor[1]) +
                '_b' + str(anchor[2]) + '_m' + str(anchor[3]) + '_1.avi')
            pos_file = (positive[0] + '_wind' + str(positive[1]) +
                '_b' + str(positive[2]) + '_m' + str(positive[3]) + '_1.avi')
            neg_file = (negative[0] + '_wind' + str(negative[1]) +
                '_b' + str(negative[2]) + '_m' + str(negative[3]) + '_1.avi')

            writer.writerow([i+1, 
                            anchor_file, pos_file, 
                            neg_file, 
                            hard_rating.total_rating(sample[i])])

'''
Converts CSV into a JSON file

Inputs:
- csv_name (string): CSV filepath
- json_name (string): JSON filepath
'''
def json_conv(csv_name, json_name):
    csv_file_path = csv_name
    json_file_path = json_name
    data = {}
    with open(csv_file_path) as testcsv:
        csvreader = csv.DictReader(testcsv)
        for row in csvreader:
            num = row['Triplet #']
            data[num] = row
    with open(json_file_path, 'w') as testjson:
        testjson.write(json.dumps(data,indent=4))


'''
Draws sample and breaks it up into smaller blocks for each participant 
to complete

Inputs:
- block_size: size of sample blocks
- k
- pct_hard
'''
def experiment(block_size, k, pct_hard):
    sample = sampling.sampler(k, pct_hard)
    block = []
    block_num = 0
    # many samples will not perfectly divide into blocks, so the remainder
    # will be distributed among the blocks
    remainder = len(sample) % block_size
    j = 0
    for i in range(math.floor(len(sample)/block_size)):
        while j < block_size:
            block.append(sample[i*block_size+j])
            j += 1
        if remainder > 0:
            block.append(sample[(i+1)*block_size])
            remainder -= 1
            j = 1
        else:
            j = 0
        csv_name = 'web_display/csv_files/block_' + str(block_num) + ".csv"
        json_name = 'web_display/json_files/block_' + str(block_num) + ".json"
        smpl_csv(block, csv_name)
        json_conv(csv_name, json_name)
        block_num += 1
        block = []


if __name__ == "__main__":
    experiment(500, 5000, 50)