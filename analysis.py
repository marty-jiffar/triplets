'''
Preliminary data analysis


Marty Jiffar
'''

import matplotlib.pyplot as plt
import math
import json
import numpy as np
from numpy.polynomial.polynomial import polyfit

def time_plot(json_path, color, block):

    with open(json_path, 'r') as f:
        data_dict = json.load(f)

    plt.plot(data_dict["trialnumber"], data_dict["time_per_trial"], color=color)

    plt.ylabel('Time (milliseconds)')
    plt.xlabel('Trial #')
    plt.title('Length of Time to Choose Video for Each Trial - Block ' + block)

    plt.xticks([0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49])
    plt.show()


def time_vs_hardness(videos_path1, data_path1,
                    videos_path2, data_path2,
                    videos_path3, data_path3,
                    videos_path4, data_path4,
                    videos_path5, data_path5,
                    videos_path6, data_path6,
                    videos_path7, data_path7,
                    videos_path8, data_path8,
                    videos_path9, data_path9,
                    videos_path10, data_path10):
    with open(videos_path1, 'r') as f:
        videos_dict1 = json.load(f)

    with open(videos_path2, 'r') as f:
        videos_dict2 = json.load(f)

    with open(videos_path3, 'r') as f:
        videos_dict3 = json.load(f)

    with open(videos_path4, 'r') as f:
        videos_dict4 = json.load(f)

    with open(videos_path5, 'r') as f:
        videos_dict5 = json.load(f)

    with open(videos_path6, 'r') as f:
        videos_dict6 = json.load(f)

    with open(videos_path7, 'r') as f:
        videos_dict7 = json.load(f)

    with open(videos_path8, 'r') as f:
        videos_dict8 = json.load(f)

    with open(videos_path9, 'r') as f:
        videos_dict9 = json.load(f)

    with open(videos_path10, 'r') as f:
        videos_dict10 = json.load(f)

    with open(data_path1, 'r') as f:
        data_dict1 = json.load(f)

    with open(data_path2, 'r') as f:
        data_dict2 = json.load(f)

    with open(data_path3, 'r') as f:
        data_dict3 = json.load(f)

    with open(data_path4, 'r') as f:
        data_dict4 = json.load(f)

    with open(data_path5, 'r') as f:
        data_dict5 = json.load(f)

    with open(data_path6, 'r') as f:
        data_dict6 = json.load(f)

    with open(data_path7, 'r') as f:
        data_dict7 = json.load(f)

    with open(data_path8, 'r') as f:
        data_dict8 = json.load(f)

    with open(data_path9, 'r') as f:
        data_dict9 = json.load(f)

    with open(data_path10, 'r') as f:
        data_dict10 = json.load(f)

    hardness_score_list1 = []
    hardness_score_list2 = []
    hardness_score_list3 = []
    hardness_score_list4 = []
    hardness_score_list5 = []
    hardness_score_list6 = []
    hardness_score_list7 = []
    hardness_score_list8 = []
    hardness_score_list9 = []
    hardness_score_list10 = []

    for x, v in videos_dict1.items():
        hardness_score_list1.append(v["Hardness Score"])

    for x, v in videos_dict2.items():
        hardness_score_list2.append(v["Hardness Score"])

    for x, v in videos_dict3.items():
        hardness_score_list3.append(v["Hardness Score"])

    for x, v in videos_dict4.items():
        hardness_score_list4.append(v["Hardness Score"])

    for x, v in videos_dict5.items():
        hardness_score_list5.append(v["Hardness Score"])

    for x, v in videos_dict6.items():
        hardness_score_list6.append(v["Hardness Score"])

    for x, v in videos_dict7.items():
        hardness_score_list7.append(v["Hardness Score"])

    for x, v in videos_dict8.items():
        hardness_score_list8.append(v["Hardness Score"])

    for x, v in videos_dict9.items():
        hardness_score_list9.append(v["Hardness Score"])

    for x, v in videos_dict10.items():
        hardness_score_list10.append(v["Hardness Score"])


    plt.scatter(sorted(hardness_score_list1), data_dict1["time_per_trial"], 
        color="red", label='Block 1')

    plt.scatter(sorted(hardness_score_list2), data_dict2["time_per_trial"], 
        color="pink", label='Block 2')

    plt.scatter(sorted(hardness_score_list3), data_dict3["time_per_trial"], 
        color="orange", label='Block 3')

    plt.scatter(sorted(hardness_score_list4), data_dict4["time_per_trial"], 
        color="yellow", label='Block 4')

    plt.scatter(sorted(hardness_score_list5), data_dict5["time_per_trial"], 
        color="blue", label='Block 5')

    plt.scatter(sorted(hardness_score_list6), data_dict6["time_per_trial"], 
        color="green", label='Block 6')

    plt.scatter(sorted(hardness_score_list7), data_dict7["time_per_trial"], 
        color="purple", label='Block 7')

    plt.scatter(sorted(hardness_score_list8), data_dict8["time_per_trial"], 
        color="black", label='Block 8')

    plt.scatter(sorted(hardness_score_list9), data_dict9["time_per_trial"], 
        color=".75", label='Block 9')

    plt.scatter(sorted(hardness_score_list10), data_dict10["time_per_trial"], 
        color=".3", label='Block 10')

    x = np.array(hardness_score_list1)
    y = np.array(data_dict1["time_per_trial"]
        + data_dict2["time_per_trial"]
        + data_dict3["time_per_trial"]
        + data_dict4["time_per_trial"]
        + data_dict5["time_per_trial"]
        + data_dict6["time_per_trial"]
        + data_dict7["time_per_trial"]
        + data_dict8["time_per_trial"]
        + data_dict9["time_per_trial"]
        + data_dict10["time_per_trial"])

    print(type(x))
    print(type(y))

    b, m = polyfit(x, y, 1)
    plt.plot(x, b + m * x, '-')


    plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
    plt.subplots_adjust(right=0.75)
    plt.ylabel('Time (milliseconds)')
    plt.xlabel('Hardness Score')
    plt.title('Length of Time to Choose Video for Each Hardness Score')

    plt.show()

if __name__ == '__main__':
    path = 'web_display/javascripts/phpcode/01_Data/'
    time_vs_hardness(path + 'Video_JSON_files/block_1.json', 
        path + 'Result_JSON_files/MP_block_1_09-17-2019_result.json',
        path + 'Video_JSON_files/block_2.json', 
        path + 'Result_JSON_files/MP_block_2_09-17-2019_result.json',
        path + 'Video_JSON_files/block_3.json', 
        path + 'Result_JSON_files/MP_block_3_09-17-2019_result.json',
        path + 'Video_JSON_files/block_4.json', 
        path + 'Result_JSON_files/MP_block_4_09-17-2019_result.json',
        path + 'Video_JSON_files/block_5.json', 
        path + 'Result_JSON_files/MP_block_5_09-17-2019_result.json',
        path + 'Video_JSON_files/block_6.json', 
        path + 'Result_JSON_files/MP_block_6_09-17-2019_result.json',
        path + 'Video_JSON_files/block_7.json', 
        path + 'Result_JSON_files/MP_block_7_09-17-2019_result.json',
        path + 'Video_JSON_files/block_8.json', 
        path + 'Result_JSON_files/MP_block_8_09-17-2019_result.json',
        path + 'Video_JSON_files/block_9.json', 
        path + 'Result_JSON_files/MP_block_9_09-17-2019_result.json',
        path + 'Video_JSON_files/block_10.json', 
        path + 'Result_JSON_files/MP_block_10_09-17-2019_result.json')
    time_plot(path + 'MP_block_2_09-17-2019_result.json', "magenta", '2')
    time_plot(path + 'MP_block_3_09-17-2019_result.json', "orange", '3')
    time_plot(path + 'MP_block_4_09-17-2019_result.json', "yellow", '4')
    time_plot(path + 'MP_block_5_09-17-2019_result.json', "green", '5')
    time_plot(path + 'MP_block_6_09-17-2019_result.json', "blue", '6')
    time_plot(path + 'MP_block_7_09-17-2019_result.json', "purple", '7')
    time_plot(path + 'MP_block_8_09-17-2019_result.json', "black", '8')
    time_plot(path + 'MP_block_9_09-17-2019_result.json', "0.75", '9')
    time_plot(path + 'MP_block_10_09-17-2019_result.json', "0.3", '10')