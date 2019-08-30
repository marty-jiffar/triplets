'''
Setting up experiment: drawing sample, dividing it into chunks,
putting chunks into CSV files and converting them to JSON files
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
            writer.writerow([i+1, 
                            sample[i][0], sample[i][1], 
                            sample[i][2], 
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
Draws sample and breaks it up into smaller chunks for each participant 
to complete

Inputs:
- size (int): size of sample chunks
- stiff
- scenes
- mass
- texture
- k
- pct_hard
'''
def experiment(size, stiff, scenes, mass, texture, k, pct_hard):
    sample = sampling.sampler(stiff, scenes, mass, texture, k, pct_hard)
    chunk = []
    chunk_num = 0
    # many samples will not perfectly divide into chunks, so the remainder
    # will be distributed among the chunks
    remainder = len(sample) % size
    j = 0
    for i in range(math.floor(len(sample)/size)):
        while j < size:
            chunk.append(sample[i*size+j])
            j += 1
        if remainder > 0:
            chunk.append(sample[(i+1)*size])
            remainder -= 1
            j = 1
        else:
            j = 0
        csv_name = 'csv_files/chunk_' + str(chunk_num) + ".csv"
        json_name = 'json_files/chunk_' + str(chunk_num) + ".json"
        smpl_csv(chunk, csv_name)
        json_conv(csv_name, json_name)
        chunk_num += 1
        chunk = []


if __name__ == "__main__":
    experiment(500, 6, 3, 7, 7, 5000, 50)