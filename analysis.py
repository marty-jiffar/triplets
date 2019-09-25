'''
Preliminary data analysis


Marty Jiffar
'''

import matplotlib.pyplot as plt
import math
import json
import numpy as np
from numpy.polynomial.polynomial import polyfit

def time_plot(json_paths, video_paths):
    for json_path in json_paths:
        with open(json_path, 'r') as f:
            data_dict = json.load(f)
            
        plt.scatter(data_dict["trialnumber"], data_dict["time_per_trial"])

    plt.ylabel('Time (milliseconds)')
    plt.xlabel('Trial #')
    plt.title('Length of Time to Choose Video for Each Trial')

    plt.xticks([0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49])
    plt.show()
    
def avg_trial_time(json_paths, video_paths, mass_variety):
    for i, json_path in enumerate(json_paths):
        with open(json_path, 'r') as f:
            data_dict = json.load(f)
        if mass_variety == 'mixed' or i < 10:
            avg = sum(data_dict["time_per_trial"]) / len(data_dict["time_per_trial"])
            variety_label = ' (50% same mass, 50% different mass)'
        else:
            time_sum = 0
            vid_path = video_paths[i]
            if mass_variety == 'same':
                same_mass_dict = same_mass(vid_path)
                group = same_mass_dict.keys()
                length = len(group)
                variety_label = ' (100% same mass)'
            else:
                diff_mass_dict = diff_mass(vid_path)
                group = diff_mass_dict.keys()
                length = len(group)
                variety_label = ' (100% different mass)'
            
            for trial in data_dict["trialnumber"]:
                if trial not in group:
                    continue
                else:
                    trial = int(trial) - 1
                    time_sum += data_dict["time_per_trial"][trial]
            
            avg = time_sum/length
        i = i % 10
        plt.scatter(i+1, avg, c='blue')
        
        
    plt.ylabel('Time (milliseconds)')
    plt.xlabel('Block #')
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.title('Avg. Time per Trial vs. Block' + variety_label)
    plt.show()

def correct_vs_wrong(json_paths, video_paths, mass_variety):
    right_v_wrong = [0, 0]
    objects = ('Correct', 'Incorrect')
    y_pos = np.arange(len(objects))
    for i, path in enumerate(json_paths):
        
        with open(path, 'r') as f:
            data_dict = json.load(f)
        
        vid_path = video_paths[i]
        
        with open(vid_path, 'r') as f:
            vid_dict = json.load(f)
        
        if mass_variety == 'mixed':
            group = range(1, len(data_dict["trialnumber"]))
            variety_label = ' (50% same mass, 50% different)'
        elif mass_variety == 'same':
            same_mass_dict = same_mass(vid_path)
            group = same_mass_dict.keys()
            variety_label = ' (100% same mass)'
        else:
            diff_mass_dict = diff_mass(video_paths[i])
            group = diff_mass_dict.keys()
            variety_label = ' (100% different mass)'
        for i in group:
            i = int(i) - 1
            if data_dict["response"][i] == data_dict["correct_answer"][i]:
                right_v_wrong[0] += 1
            else:
                right_v_wrong[1] += 1
        
    plt.bar(y_pos, right_v_wrong, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('# of Trials')
    plt.title('Correct vs. Incorrect' + variety_label)
    print('bar graph 1: ')
    print(right_v_wrong[0] + right_v_wrong[1])
    print('num correct: ' + str(right_v_wrong[0]))
    print('num incorrect: ' + str(right_v_wrong[1]))

    
    plt.show()
    
def stacked_correctpct_vs_hard(json_paths, video_paths, mass_variety):
    n = 11
    ind = np.arange(n)
    correct = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    incorrect = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                
    for i, path in enumerate(json_paths):
        if ((i + 1) % 10 == 0):
            block = 10
        else: 
            block = (i + 1) % 10
        
        with open(path, 'r') as f:
            data_dict = json.load(f)
            
        with open(video_paths[i], 'r') as f:
            vid_dict = json.load(f)
        
        if mass_variety == 'mixed':
            group = range(1, len(data_dict["trialnumber"]) + 1)
            variety_label = ' (50% same mass, 50% different mass)'
            
        elif mass_variety == 'same':
            same_mass_dict = same_mass(video_paths[i])
            group = same_mass_dict.keys()
            variety_label = ' (100% same mass)'
        
        else:
            diff_mass_dict = diff_mass(video_paths[i])
            group = diff_mass_dict.keys()
            variety_label = ' (100% different mass)'
                          
        for i in group:
            i = int(i) - 1
            hard_score = int(vid_dict[str(i+1)]["Hardness Score"])
            if data_dict["response"][i] == data_dict["correct_answer"][i]:
                correct[hard_score] += 1
            else:
                incorrect[hard_score] += 1
    '''
    p1 = plt.bar(ind, correct)
    p2 = plt.bar(ind, incorrect, bottom=correct)
    
    print('bar graph 2: ')
    print(sum(correct) + sum(incorrect))
    print('num correct: ' + str(sum(correct)))
    print('num incorrect: ' + str(sum(incorrect)))
    
    plt.ylabel('Correct vs. Incorrect (# of Trials)')
    plt.title('Correct vs Incorrect Trials by Hardness' + variety_label)
    plt.legend((p1[0], p2[0]), ('Correct', 'Incorrect'))
    plt.xlabel('Hardness Score')
    '''
    if mass_variety == 'mixed':
       # plt.yticks(np.arange(0, 321, 20))
        y = [20, 80, 150, 220, 250, 245, 270, 210, 120, 45, 10]
    elif mass_variety == 'same':
      #  plt.yticks(np.arange(0, 121, 10))
        y = [10, 50, 65, 80, 86, 100, 86, 61, 10, 5, 5]
    else:
      #  plt.yticks(np.arange(0, 201, 20))
        y = [5, 25, 80, 140, 160, 145, 187, 147, 110, 37, 5]
    
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
    
    print(sums)
    '''
    plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
         [correct[0], correct[1], correct[2], correct[3],
         correct[4], correct[5], correct[6], correct[7],
         correct[8], correct[9], correct[10]], marker='o', color = 'b')
    '''
    xpos = -.45
    pct_correct = []
    for i, val in enumerate(sums):
        if sums[i] > 0:
           # plt.text(xpos, y[i], str(round(correct[i] / sums[i] * 100, 1)) + '%')
            pct_correct.append(round(correct[i] / sums[i] * 100, 1))
        else:
            pct_correct.append(0)
            
        xpos += 1
    
  #  plt.show()
    
    
    plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], pct_correct, marker='o', color = 'b')
    plt.ylabel('Correct vs. Incorrect (% of Trials)')
    plt.yticks(np.arange(0, 101, 10))
    plt.xlabel('Hardness Score')
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.title('% Correct Trials by Hardness' + variety_label)
    plt.show()
    
    plt.show()
    
def stacked_correctpct_vs_block(json_paths, video_paths, mass_variety):
    n = 10
    ind = np.arange(1, n+1)
    correct = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    incorrect = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    for i, path in enumerate(json_paths):
        if ((i + 1) % 10 == 0):
            block = 10
        else: 
            block = (i + 1) % 10
        
        with open(path, 'r') as f:
            data_dict = json.load(f)
            
        with open(video_paths[i], 'r') as f:
            vid_dict = json.load(f)
        
        if mass_variety == 'mixed':
            group = range(1, len(data_dict["trialnumber"]) + 1)
            variety_label = ' (50% same mass, 50% different mass)'
            
        elif mass_variety == 'same':
            same_mass_dict = same_mass(video_paths[i])
            group = same_mass_dict.keys()
            variety_label = ' (100% same mass)'
        
        else:
            diff_mass_dict = diff_mass(video_paths[i])
            group = diff_mass_dict.keys()
            variety_label = ' (100% different mass)'
                          
        for i in group:
            i = int(i) - 1
            if data_dict["response"][i] == data_dict["correct_answer"][i]:
                correct[block-1] += 1
            else:
                incorrect[block-1] += 1
    
    '''
    p1 = plt.bar(ind, correct, label='Correct')
    p2 = plt.bar(ind, incorrect, bottom=correct, label='Incorrect')
    
    print('bar graph 2: ')
    print(sum(correct) + sum(incorrect))
    print('num correct: ' + str(sum(correct)))
    print('num incorrect: ' + str(sum(incorrect)))
    
    plt.ylabel('Correct vs. Incorrect (# of Trials)')
    plt.xlabel('Block #')
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.title('Correct vs Incorrect Trials by Block' + variety_label)
    '''
    if mass_variety == 'same':
        plt.yticks(np.arange(0, 71, 10))
        y = 15
    elif mass_variety == 'different':
        plt.yticks(np.arange(0, 131, 10))
        y = 30
    else:
        plt.yticks(np.arange(0, 181, 20))
        y = 60 
        
   # plt.legend((p1[0], p2[0]), ('Correct', 'Incorrect'))
   # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
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
    '''
    plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
             [correct[0], correct[1], correct[2], correct[3],
             correct[4], correct[5], correct[6], correct[7],
             correct[8], correct[9]], marker='o', color = 'b')
    '''
    xpos = 0.65
    pct_correct = []
    for i, val in enumerate(sums):
        if sums[i] > 0:
         #   plt.text(xpos, y, str(round(correct[i] / sums[i] * 100, 1)) + '%', fontsize = 7.5)
            pct_correct.append(round(correct[i] / sums[i] * 100, 1))
        else:
            pct_correct.append(0)
        
        xpos += 1
    
   # plt.show()

    
    plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], pct_correct, marker='o', color = 'b')
    plt.ylabel('Correct vs. Incorrect (% of Trials)')
    plt.yticks(np.arange(30, 81, 10))
    plt.xlabel('Block #')
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.title('% Correct Trials by Block' + variety_label)
    plt.show()
    
def same_mass(json_path):
    with open(json_path, 'r') as f:
        data_dict = json.load(f)

    same_mass_dict = {}

    for i in range(len(data_dict.items())):
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

def diff_mass(json_path):
    with open(json_path, 'r') as f:
        data_dict = json.load(f)

    diff_mass_dict = {}

    for i in range(len(data_dict.items())):
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

        if (anchor_mass != pos_mass or 
            anchor_mass != neg_mass or 
            pos_mass != neg_mass):
            diff_mass_dict[str(i+1)] = data_dict[str(i+1)]
        
    return diff_mass_dict
    
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
    
    #time_plot(result_paths)
    
    #time_vs_hardness(video_paths, result_paths)

    #correct_vs_wrong(result_paths, video_paths, 'mixed')
    
    #correct_vs_wrong(result_paths, video_paths, 'same')
    
   # correct_vs_wrong(result_paths, video_paths, 'different')
    
    #stacked_correctpct_vs_hard(result_paths)
    
    avg_trial_time(result_paths, video_paths, 'mixed')
    
    avg_trial_time(result_paths, video_paths, 'same')
    
    avg_trial_time(result_paths, video_paths, 'different')
    
    stacked_correctpct_vs_block(result_paths, video_paths, 'mixed')
                          
    stacked_correctpct_vs_block(result_paths, video_paths, 'same')
    
    stacked_correctpct_vs_block(result_paths, video_paths, 'different')
    
    stacked_correctpct_vs_hard(result_paths, video_paths, 'mixed')
    
    stacked_correctpct_vs_hard(result_paths, video_paths, 'same')
    
    stacked_correctpct_vs_hard(result_paths, video_paths, 'different')
    
    #same_dict = same_mass(video_paths[11])
    
    #print(same_dict.items())
    
