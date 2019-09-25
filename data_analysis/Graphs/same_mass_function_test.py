'''
Analyzer

Marty Jiffar
'''

import experiment_preparer
import json

def same_mass(json_path):
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


if __name__ == '__main__':
    path1 = 'web_display/javascripts/phpcode/02_Data/'
    test_path = path1 + 'Video_JSON_files/block_1.json'
    same_mass(test_path)