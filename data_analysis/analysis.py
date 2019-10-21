'''
Preliminary data analysis


Marty Jiffar
'''


import matplotlib.pyplot as plt
import math
import json
import numpy as np
import pandas as pd
from numpy.polynomial.polynomial import polyfit
import sklearn
from sklearn.metrics import confusion_matrix
import seaborn as sns
import statistics as st
import os



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
            variety_label = ' (all data)'
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
            variety_label = ' (all data)'
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
            variety_label = ' (all data)'
            
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
            variety_label = ' (all data)'
            
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
        
        data_dict = data_paths[i]

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
    
def hist_correct(same_500_data, NN_results):
    pct_correct = []
            
    num_of_people = len(same_500_data) // 10
    print("number of ppl: " + str(num_of_people))
    data_paths = []
    data_dicts = []
    
    print('data dicts:')
    
    for data_path in same_500_data:
        with open(data_path, 'r') as f:
            data_dicts.append(json.load(f))
            print(data_dicts[-1])
    
    with open(NN_results, 'r') as f:
        NN_dict = json.load(f)
    
    print(NN_dict)
    
    pcts = ('0%', '25%', '50%', '75%', '100%')
    y_pos = np.arange(len(pcts))
    pct_freq = [0, 0, 0, 0, 0]
    computer = [0, 0, 0, 0, 0]
    
    total_correct = 0
    total_NN_correct = 0
    
    for block in range(10):
        for trial in range(50):
            correct_sum = 0
            for i in range(num_of_people):
                if (data_dicts[block + 10 * i]["response"][trial] == 
                    data_dicts[block + 10 * i]["correct_answer"][trial]):
                    correct_sum += 1
                    total_correct += 1
            pct_correct = correct_sum / 4
            
            computer_correct = (NN_dict[str(block+1)]["response"][trial] == 
                                int(NN_dict[str(block+1)]["correct_answer"][trial]))
            
            if (computer_correct):
                total_NN_correct += 1
                
            if (pct_correct == 0.0):
                pct_freq[0] += 1
                if (computer_correct):
                    computer[0] += 1
            elif (pct_correct == 0.25):
                pct_freq[1] += 1
                if (computer_correct):
                    computer[1] += 1
            elif (pct_correct == 0.50):
                pct_freq[2] += 1
                if (computer_correct):
                    computer[2] += 1
            elif (pct_correct == 0.75):
                pct_freq[3] += 1
                if (computer_correct):
                    computer[3] += 1
            elif (pct_correct == 1.00):
                pct_freq[4] += 1
                if (computer_correct):
                    computer[4] += 1
            print('------ NEW TRIAL ------')
            
    correct_total_pct = total_correct / 2000
    NN_total_pct = total_NN_correct / 500
    
    print("total correct %: " + str(correct_total_pct))
    print("NN correct %: " + str(NN_total_pct))
            
    print("computer % in each bar: ") 
    print("0%: " + str(computer[0] / pct_freq[0]))
    print("25%: " + str(computer[1] / pct_freq[1]))
    print("50%: " + str(computer[2] / pct_freq[2]))
    print("75%: " + str(computer[3] / pct_freq[3]))
    print("100%: " + str(computer[4] / pct_freq[4]))
        
    plot_humans = plt.bar(y_pos, pct_freq, align = 'center', alpha = 0.5, color = '#FF0000')
    plot_computer = plt.bar(y_pos, computer, align = 'center', alpha = 0.5, color = '#00FF00')
    plt.xticks(y_pos, pcts)
    plt.ylabel('Trials')
    plt.title('Percentage of Correct Responses per trial')
    plt.show()
    
def plot_confusion_matrix(same_500_data, NN_results):
    #pct_correct = []
            
    num_of_people = len(same_500_data) // 10
    data_paths = []
    data_dicts = []
    
    for data_path in same_500_data:
        with open(data_path, 'r') as f:
            data_dicts.append(json.load(f))
    
    with open(NN_results, 'r') as f:
        NN_dict = json.load(f)
        
    human_response_data = [[], [], [], []]
    ground_truth = []
    NN_response_data = []
    
    for block in range(10):
        for i in range(num_of_people):
            human_response_data[i] += data_dicts[block + 10 * i]["response"]
        ground_truth += data_dicts[block]["correct_answer"]
        NN_response_data += NN_dict[str(block + 1)]["response"]
            
    print(str(len(human_response_data)))
    print(str(len(human_response_data[0])))
    print(len(ground_truth))
    print(len(NN_response_data))
    
    for i in range(num_of_people):
        matrix = confusion_matrix(ground_truth, human_response_data[i], ["-1", "1"])
        sns.heatmap(matrix, vmin = 100, vmax = 160, annot = True, fmt="d", xticklabels = ["-1", "1"], 
                yticklabels = ["-1", "1"], cmap="Greys")
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.title('Participant ' + str(i + 1))
        plt.show()
    

    nn_cm = confusion_matrix(ground_truth, NN_response_data, ["-1", "1"])
    
  #  pal = sns.dark_palette("white", as_cmap=True)
    
    sns.heatmap(nn_cm, vmin = 100, vmax = 160, annot = True, fmt="d", xticklabels = ["-1", "1"], 
                yticklabels = ["-1", "1"], cmap="Greys")
    
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.title('Neural Network')
    plt.show()
    
    
def right_conf_matrices(same_videos, result_paths):
    
    # add all video names to list
    directory = os.fsencode("../web_display/Final_Dataset_6sec_mp4")
    all_videos = []
    data = {}
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        all_videos.append(filename) # all video filenames, 882 of them
        data[filename] = 882 * [-999] # initializing empty columns of dataframe
    '''
    cols = all_videos
    data = np.zeros((882, 882))
    data[new_array == 0] = -999
    '''
    
    results = []
    
    for result in result_paths:
        with open(result, 'r') as f:
            results.append(json.load(f)) # participant results, rn results is TM block 1 to 10
        
    vid_dicts = [] 
    
    for video in same_videos:
        with open(video, 'r') as f:
            vid_dicts.append(json.load(f)) # videos loaded properly
        
    df = pd.DataFrame(data, index = all_videos) # 882 by 882 dataframe, labeled with video names,
                                                # diagonal is where row video = column video
    
    for block in range(10):
        for trial in range(50): # iterating thru each triplet
            anchor = vid_dicts[block][str(trial + 1)]["Anchor"]
            pos = vid_dicts[block][str(trial + 1)]["Positive"]
            neg = vid_dicts[block][str(trial + 1)]["Negative"]
            
            print('df.loc[anchor, pos]: ' + str(df.loc[anchor, pos]))
            
            anch_pos_grouped = int(results[block]["response"][trial] 
                                == results[block]["correct_answer"][trial]) # anchor grouped w pos if user was correct
            anch_neg_grouped = int(not (anch_pos_grouped)) # otherwise, anchor grouped w neg
            
            if df.loc[anchor, pos] == -999:
                df.loc[anchor, pos] = [anch_pos_grouped]
            else:
                df.loc[anchor, pos].append(anch_pos_grouped) # creates list of groupings (1 or 0, grouped or not)
                
            if df.loc[anchor, neg] == -999:
                df[anchor][neg] = [anch_neg_grouped]
            else:
                df.loc[anchor, neg].append(anch_neg_grouped)
                
                
    for row in all_videos:
        for col in all_videos:
            if col == row:
                df.loc[row, col] = 1.0 # set pairwise similarity on diag to be 1.0
            else:
                if (df.loc[row, col] == -999) and (df.loc[col, row] == -999): # if the pair has no occurrences, skip
                    continue
                elif (df.loc[row, col] == -999 and df.loc[col, row] != -999): # current space null, diag not null
                    df.loc[row, col] = df.loc[col, row]
                elif (df.loc[row, col] != -999 and df.loc[col, row] == -999): # current space not null, diag null
                    df.loc[col, row] = df.loc[row, col]
                else: # both current space and diag are lists of legitimate numbers
                    print('[row, col]: ' + str(df.loc[row, col]))
                    print('[col, row]: ' + str((df.loc[col, row])))
                    mean = st.mean(df.loc[row, col] + df.loc[col, row])
                    df.loc[row, col] = mean
                    df.loc[col, row] = mean
    
    sns.heatmap(df, annot = True, fmt="d", cmap="Blues")
    
    plt.ylabel('Video Names')
    plt.xlabel('Video Names')
    plt.title('Pairwise Similarity')
    plt.show()
    
    
    
            
    
if __name__ == '__main__':
    path_start = '../web_display/javascripts/phpcode/'
    folders = ['01_Data/', '02_Data/', '03_Data/', '04_Data/', '05_Data/', '06_Data/']
    res_string = 'Result_JSON_files/'
    
    initials = ['MP', 'TM', 'OF', 'or', 'FR', 'MY']
    blocks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    dates = ['09-17-2019', '09-19-2019', '09-24-2019', '09-27-2019']
    
    result_paths = []
    same_500_results = []
    
    for i in range(len(folders)):
        if i == 0:
            date = dates[0]
        elif i < 3:
            date = dates[1]
        elif i < 5:
            date = dates[2]
        else:
            date = dates[3]
        for block_num in blocks:
            current_path = (path_start + folders[i] + res_string + initials[i] + '_block_' + block_num
                + '_' + date + '_result.json')
            result_paths.append(current_path)
            if (i == 1 or i == 3 or i == 4 or i == 5):
                same_500_results.append(current_path) # results that came from the same 500 videos
            
    vid_path = 'Video_JSON_files/block_'
    video_paths = []
    
    for i in range(len(folders)):
        for block_num in blocks:
            current_path = (path_start + folders[i] + vid_path + block_num + '.json')
            video_paths.append(current_path)
            
    mass_varieties = ['mixed', 'same', 'different']
    '''
    for mass_setting in mass_varieties:
        correct_vs_wrong(result_paths, video_paths, mass_setting)
        avg_trial_time(result_paths, video_paths, mass_setting)
        stacked_correctpct_vs_block(result_paths, video_paths, mass_setting)
        stacked_correctpct_vs_hard(result_paths, video_paths, mass_setting)
    '''
    
    same_video_paths = video_paths[10:20]
    
    NN_results = path_start + 'NN_Data/NN_10_18_2019_result.json'
    
    #hist_correct(same_video_paths, same_500_results, NN_results)
    
    #print("len same results: " + str(len(same_500_results)))
    
    plot_confusion_matrix(same_500_results, NN_results)
    
    #time_vs_hardness(video_paths, result_paths)
    
    #right_conf_matrices(same_video_paths, same_500_results[0:10])
    