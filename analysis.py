'''
Preliminary data analysis


Marty Jiffar
'''

import matplotlib.pyplot as plt
import math
import json
import numpy as np
from numpy.polynomial.polynomial import polyfit

def time_plot(json_paths):
    for json_path in json_paths:
        with open(json_path, 'r') as f:
            data_dict = json.load(f)

        plt.scatter(data_dict["trialnumber"], data_dict["time_per_trial"])

    plt.ylabel('Time (milliseconds)')
    plt.xlabel('Trial #')
    plt.title('Length of Time to Choose Video for Each Trial')

    plt.xticks([0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49])
    plt.show()
    
def avg_trial_time(json_paths):
    for i, json_path in enumerate(json_paths):
        with open(json_path, 'r') as f:
            data_dict = json.load(f)
        
        avg = sum(data_dict["time_per_trial"]) / len(data_dict["time_per_trial"])
        
        plt.scatter(i+1, avg)
    plt.ylabel('Time (milliseconds)')
    plt.xlabel('Block #')
    plt.title('Avg. Time per Trial vs. Block')
    plt.show()

def correct_vs_wrong(json_paths):
    right_v_wrong = [0, 0]
    objects = ('Correct', 'Incorrect')
    y_pos = np.arange(len(objects))
    for i, path in enumerate(json_paths):
        
        with open(path, 'r') as f:
            data_dict = json.load(f)
        
        
        
        for i in range(len(data_dict["trialnumber"])):
            if data_dict["response"][i] == data_dict["correct_answer"][i]:
                right_v_wrong[0] += 1
            else:
                right_v_wrong[1] += 1
        
    plt.bar(y_pos, right_v_wrong, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('# of Trials')
    plt.title('Correct vs. Incorrect')
    print('bar graph 1: ')
    print(right_v_wrong[0] + right_v_wrong[1])
    print('num correct: ' + str(right_v_wrong[0]))
    print('num incorrect: ' + str(right_v_wrong[1]))
    
   
    plt.text(300, 300, str(round(right_v_wrong[1]/
                                (right_v_wrong[0] + right_v_wrong[1])* 100, 1)))
    
    plt.show()
    
def stacked_correctpct_vs_hard(json_paths):
    n = 11
    ind = np.arange(n)
    correct = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    incorrect = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    block = None
    for i, path in enumerate(json_paths):
        vid_path = path[0:40]
        if ((i + 1) % 10 == 0):
            block = 10
        else: 
            block = int(path[67])
        full_vid_path = vid_path + 'Video_JSON_files/block_' + str(block) + '.json'
        
        with open(path, 'r') as f:
            data_dict = json.load(f)
            
        with open(full_vid_path, 'r') as f:
            vid_dict = json.load(f)
        
        for i in range(len(data_dict["trialnumber"])):
            hard_score = int(vid_dict[str(i+1)]["Hardness Score"])
            if data_dict["response"][i] == data_dict["correct_answer"][i]:
                correct[hard_score] += 1
            else:
                incorrect[hard_score] += 1
                
    p1 = plt.bar(ind, correct)
    p2 = plt.bar(ind, incorrect, bottom=correct)
    
    print('bar graph 2: ')
    print(sum(correct) + sum(incorrect))
    print('num correct: ' + str(sum(correct)))
    print('num incorrect: ' + str(sum(incorrect)))
    
    plt.ylabel('Correct vs. Incorrect')
    plt.title('% Correct Trials by Hardness Score')
    plt.yticks(np.arange(0, 321, 20))
    plt.legend((p1[0], p2[0]), ('Correct', 'Incorrect'))
    
    sums = [correct[0] + incorrect[0],
           correct[1] + incorrect[1],
           correct[2] + incorrect[2],
           correct[3] + incorrect[3],
           correct[4] + incorrect[4],
           correct[5] + incorrect[5],
           correct[6] + incorrect[6],
           correct[7] + incorrect[7],
           correct[8] + incorrect[8],
           correct[9] + incorrect[9],
           correct[10] + incorrect[10]]
    
    plt.text(-0.25, 20, str(round(correct[0]/sums[0] * 100, 1)))
    plt.text(0.5, 80, str(round(correct[1]/sums[1] * 100, 1)))
    plt.text(1.5, 150, str(round(correct[2]/sums[2] * 100, 1)))
    plt.text(2.5, 220, str(round(correct[3]/sums[3] * 100, 1)))
    plt.text(3.5, 250, str(round(correct[4]/sums[4] * 100, 1)))
    plt.text(4.5, 245, str(round(correct[5]/sums[5] * 100, 1)))
    plt.text(5.5, 280, str(round(correct[6]/sums[6] * 100, 1)))
    plt.text(6.5, 210, str(round(correct[7]/sums[7] * 100, 1)))
    plt.text(7.5, 120, str(round(correct[8]/sums[8] * 100, 1)))
    plt.text(8.5, 45, str(round(correct[9]/sums[9] * 100, 1)))
    plt.text(9.5, 10, str(round(correct[10]/sums[10] * 100, 1)))
    
    plt.show()
    
def stacked_correctpct_vs_block(json_paths):
    n = 10
    ind = np.arange(n)
    correct = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    incorrect = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    block = None
    for i, path in enumerate(json_paths):
        vid_path = path[0:40]
        if ((i + 1) % 10 == 0):
            block = 10
        else: 
            block = int(path[67])
        full_vid_path = vid_path + 'Video_JSON_files/block_' + str(block) + '.json'
        
        with open(path, 'r') as f:
            data_dict = json.load(f)
            
        with open(full_vid_path, 'r') as f:
            vid_dict = json.load(f)
        
        for i in range(len(data_dict["trialnumber"])):
            if data_dict["response"][i] == data_dict["correct_answer"][i]:
                correct[block-1] += 1
            else:
                incorrect[block-1] += 1
                
    p1 = plt.bar(ind, correct, label='Correct')
    p2 = plt.bar(ind, incorrect, bottom=correct, label='Incorrect')
    
    print('bar graph 2: ')
    print(sum(correct) + sum(incorrect))
    print('num correct: ' + str(sum(correct)))
    print('num incorrect: ' + str(sum(incorrect)))
    
    plt.ylabel('Correct vs. Incorrect')
    plt.xlabel('Block #')
    plt.title('% Correct Trials by Block')
    plt.yticks(np.arange(0, 181, 20))
    plt.legend((p1[0], p2[0]), ('Correct', 'Incorrect'))
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    sums = [correct[0] + incorrect[0],
           correct[1] + incorrect[1],
           correct[2] + incorrect[2],
           correct[3] + incorrect[3],
           correct[4] + incorrect[4],
           correct[5] + incorrect[5],
           correct[6] + incorrect[6],
           correct[7] + incorrect[7],
           correct[8] + incorrect[8],
           correct[9] + incorrect[9]]
    
    plt.text(-0.25, 155, str(round(correct[0]/sums[0] * 100, 1)))
    plt.text(0.75, 155, str(round(correct[1]/sums[1] * 100, 1)))
    plt.text(1.75, 155, str(round(correct[2]/sums[2] * 100, 1)))
    plt.text(2.75, 155, str(round(correct[3]/sums[3] * 100, 1)))
    plt.text(3.75, 155, str(round(correct[4]/sums[4] * 100, 1)))
    plt.text(4.75, 155, str(round(correct[5]/sums[5] * 100, 1)))
    plt.text(5.75, 155, str(round(correct[6]/sums[6] * 100, 1)))
    plt.text(6.75, 155, str(round(correct[7]/sums[7] * 100, 1)))
    plt.text(7.75, 155, str(round(correct[8]/sums[8] * 100, 1)))
    plt.text(8.75, 155, str(round(correct[9]/sums[9] * 100, 1)))
    
    plt.show()
    
def same_mass(json_paths):
    for path in json_paths:
        with open(json_path, 'r') as f:
            data_dict = json.load(f)

        same_mass_dict = {}

        for i in range(len(data_dict.items())):
            print(i)
            anchor_mass_ind = data_dict[str(i+1)]["Anchor"].find("_m")
            pos_mass_ind = data_dict[str(i+1)]["Positive"].find("_m")
            neg_mass_ind = data_dict[str(i+1)]["Negative"].find("_m")

            if (data_dict[str(i+1)]["Anchor"][anchor_mass_ind + 3] == '_'):
                anchor_mass = '1'
            else:
                anchor_mass = data_dict[str(i+1)]["Anchor"][anchor_mass_ind + 2:
                                                         anchor_mass_ind + 5]
            if (data_dict[str(i+1)]["Positive"][pos_mass_ind + 3] == '_'):
                pos_mass = '1'
            else:
                pos_mass = data_dict[str(i+1)]["Positive"][pos_mass_ind + 2:
                                                         pos_mass_ind + 5]
            if (data_dict[str(i+1)]["Negative"][neg_mass_ind + 3] == '_'):
                neg_mass = '1'
            else:
                neg_mass = data_dict[str(i+1)]["Negative"][neg_mass_ind + 2:
                                                         neg_mass_ind + 5]

            if anchor_mass == pos_mass == neg_mass:
                same_mass_dict[str(i+1)] = data_dict[str(i+1)]
        
    return same_mass_dict
    
def time_vs_hardness(video_paths, data_paths):
    
    for i, video_path in enumerate(video_paths):
        with open(video_path, 'r') as f:
            videos_dict = json.load(f)
        
        data_path = data_paths[i]
        
        with open(data_path, 'r') as f:
            data_dict = json.load(f)

        hardness_score_list = []

        for x, v in videos_dict.items():
            hardness_score_list.append(v["Hardness Score"])


        plt.scatter(sorted(hardness_score_list), data_dict["time_per_trial"], 
            color="blue")

        x = np.array(hardness_score_list)
        y = np.array(data_dict["time_per_trial"])

    print(type(x))
    print(type(y))
    plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
    plt.subplots_adjust(right=0.75)
    plt.ylabel('Time (milliseconds)')
    plt.xlabel('Hardness Score')
    plt.title('Length of Time to Choose Video for Each Hardness Score')

    plt.show()

if __name__ == '__main__':
    path1 = 'web_display/javascripts/phpcode/01_Data/'
    path2 = 'web_display/javascripts/phpcode/02_Data/'
    path3 = 'web_display/javascripts/phpcode/03_Data/'
    
    result_paths = [path1 + 'Result_JSON_files/MP_block_1_09-17-2019_result.json',
             path1 + 'Result_JSON_files/MP_block_2_09-17-2019_result.json', 
             path1 + 'Result_JSON_files/MP_block_3_09-17-2019_result.json', 
             path1 + 'Result_JSON_files/MP_block_4_09-17-2019_result.json', 
             path1 + 'Result_JSON_files/MP_block_5_09-17-2019_result.json', 
             path1 + 'Result_JSON_files/MP_block_6_09-17-2019_result.json', 
             path1 + 'Result_JSON_files/MP_block_7_09-17-2019_result.json', 
             path1 + 'Result_JSON_files/MP_block_8_09-17-2019_result.json', 
             path1 + 'Result_JSON_files/MP_block_9_09-17-2019_result.json', 
             path1 + 'Result_JSON_files/MP_block_10_09-17-2019_result.json',
             path2 + 'Result_JSON_files/TM_block_1_09-19-2019_result.json',
             path2 + 'Result_JSON_files/TM_block_2_09-19-2019_result.json', 
             path2 + 'Result_JSON_files/TM_block_3_09-19-2019_result.json', 
             path2 + 'Result_JSON_files/TM_block_4_09-19-2019_result.json', 
             path2 + 'Result_JSON_files/TM_block_5_09-19-2019_result.json', 
             path2 + 'Result_JSON_files/TM_block_6_09-19-2019_result.json', 
             path2 + 'Result_JSON_files/TM_block_7_09-19-2019_result.json', 
             path2 + 'Result_JSON_files/TM_block_8_09-19-2019_result.json', 
             path2 + 'Result_JSON_files/TM_block_9_09-19-2019_result.json', 
             path2 + 'Result_JSON_files/TM_block_10_09-19-2019_result.json',
             path3 + 'Result_JSON_files/OF_block_1_09-19-2019_result.json',
             path3 + 'Result_JSON_files/OF_block_2_09-19-2019_result.json', 
             path3 + 'Result_JSON_files/OF_block_3_09-19-2019_result.json', 
             path3 + 'Result_JSON_files/OF_block_4_09-19-2019_result.json', 
             path3 + 'Result_JSON_files/OF_block_5_09-19-2019_result.json', 
             path3 + 'Result_JSON_files/OF_block_6_09-19-2019_result.json', 
             path3 + 'Result_JSON_files/OF_block_7_09-19-2019_result.json', 
             path3 + 'Result_JSON_files/OF_block_8_09-19-2019_result.json', 
             path3 + 'Result_JSON_files/OF_block_9_09-19-2019_result.json', 
             path3 + 'Result_JSON_files/OF_block_10_09-19-2019_result.json']
    
    block1path = 'Video_JSON_files/block_1.json'
    block2path = 'Video_JSON_files/block_2.json'
    block3path = 'Video_JSON_files/block_3.json'
    block4path = 'Video_JSON_files/block_4.json'
    block5path = 'Video_JSON_files/block_5.json'
    block6path = 'Video_JSON_files/block_6.json'
    block7path = 'Video_JSON_files/block_7.json'
    block8path = 'Video_JSON_files/block_8.json'
    block9path = 'Video_JSON_files/block_9.json'
    block10path = 'Video_JSON_files/block_10.json'
    
    video_paths = [path1 + block1path,
             path1 + block2path, 
             path1 + block3path, 
             path1 + block4path, 
             path1 + block5path, 
             path1 + block6path, 
             path1 + block7path, 
             path1 + block8path, 
             path1 + block9path, 
             path1 + block10path,
             path2 + block1path,
             path2 + block2path, 
             path2 + block3path, 
             path2 + block4path, 
             path2 + block5path, 
             path2 + block6path, 
             path2 + block7path, 
             path2 + block8path, 
             path2 + block9path, 
             path2 + block10path,
             path3 + block1path,
             path3 + block2path, 
             path3 + block3path, 
             path3 + block4path, 
             path3 + block5path, 
             path3 + block6path, 
             path3 + block7path, 
             path3 + block8path, 
             path3 + block9path, 
             path3 + block10path]
    
    time_plot(result_paths)
    
    time_vs_hardness(video_paths, result_paths)

    correct_vs_wrong(result_paths)
    
    stacked_correctpct_vs_hard(result_paths)
    
    stacked_correctpct_vs_block(result_paths)
    
