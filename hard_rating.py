'''
A group of functions to quantify how easy it is to differentiate negative
videos. Four ratings are generated for based on how the videos in the triplet
compare to one another in stiffness, scene, mass, and texture. At the end
these ratings are added together.

Inputs:
- triplet (tuple of tuples): positive, anchor, and negative

Returns:
- points (int): number representing ease of assessment (higher means harder)
'''
def stiff_rating(triplet):
    points = 0
    anchor = triplet[0]
    negative = triplet[2]
    stiff_diff = abs(anchor[0] - negative[0]) 

    # the larger the difference, the easier 
    # it is to pick out the negative
    if stiff_diff == 4:
        points += 1 
    elif stiff_diff == 3:
        points += 2
    elif stiff_diff == 2:
        points += 3
    elif stiff_diff == 1:
        points += 4
    return points

def scene_rating(triplet):
    points = 0
    anchor = triplet[0]
    positive = triplet[1]
    negative = triplet[2]

    # medium difficulty when all scenes are different
    if (anchor[1] != positive[1] != negative[1]):
        points += 1
    # greater difficulty when negative matches with 
    # anchor or positive
    elif ((anchor[1] == negative[1] != positive[1]) or 
         (positive[1] == negative[1] != anchor[1])):
        points += 2
    return points

def mass_rating(triplet):
    points = 0
    anchor = triplet[0]
    positive = triplet[1]
    negative = triplet[2]
    diff_pos_neg = abs(positive[2] - negative[2])
    diff_anch_neg = abs(anchor[2] - negative[2])
    diff_pos_anch = abs(anchor[2] - positive[2])
    if (anchor[2] != positive[2] != negative[2]):
        points += 1
        # greater difficulty if the anchor's mass is closer
        # to the negative's mass than the positive's
        if (diff_anch_neg < diff_pos_anch):
            points += 1
    # greater difficulty if the negative matches anchor/positive,
    # while the positive/anchor is a very different mass
    elif (anchor[2] == negative[2] != positive[2]
        and diff_pos_neg >= 2):
        points += 3
        if diff_pos_neg >= 4:
            points += 1
    elif (positive[2] == negative[2] != anchor[2]
        and diff_anch_neg >= 2):
        points += 3
        if diff_anch_neg >= 4:
            points += 1
    return points

def texture_rating(triplet):
    points = 0
    anchor = triplet[0]
    positive = triplet[1]
    negative = triplet[2]
    # medium difficulty when all textures are different
    if (anchor[3] != positive[3] != negative[3]):
        points += 1
    # greater difficulty when negative matches
    # with anchor/positive
    elif ((anchor[3] == negative[3] != positive[3]) or
         (positive[3] == negative[3] != anchor[3])):
        points += 2
    return points

def total_rating(triplet):
    total_rating = (stiff_rating(triplet) + scene_rating(triplet)
                + mass_rating(triplet) + texture_rating(triplet))
    return total_rating
