"""

Compare with gold standard

1. Parse gold standard site file, create list of gold standard points
2. Mark each line in output as either gold-standard positive or negative
3. Go down the array until you hit a sensitivity of 99%
4. (later) graph the ROC curve

"""

import math
import matplotlib.pyplot as plt
import numpy as np
import os

GOLD_STANDARD_SITE = "/home/katz/Code/cs279proj/eval/calciums.CA.site"
# hits file, sorted from highest score (most likely to be a hit) to lowest
OUT_DIR = "/home/katz/Code/cs279proj/out"

# max distance for each point
HIT_ANGSTROM_MAX_DISTANCE = 3

# create gold standard dict
gold = {}
with open(GOLD_STANDARD_SITE, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(" ")
            pdb_id = line[0].split('"')[1].lower()
            x, y, z = (float(line[2]), float(line[4]), float(line[6]))
            
            if pdb_id not in gold:
                gold[pdb_id] = []
            gold[pdb_id].append((x, y, z))

def is_hit(pdb_id, x, y, z):
        true_positives = gold[pdb_id]
        for i in range(len(true_positives)):
            point = true_positives[i]
            max_distance = max([abs(x - point[0]), abs(y - point[1]), abs(z - point[2])])
            if max_distance < HIT_ANGSTROM_MAX_DISTANCE:
                return i
        return -1

actual_negatives = 0
with open("/home/katz/Code/cs279proj/tmp/out/4-1.25-5-gauss-expr/hits.sorted", "r") as f:
        lines = f.readlines()
        total = len(lines)
        actual_negatives = 0
        # count number of true positives -- ie calcium binding sites
        for line in lines:
            line = line.split("\t")
            pdb_id = line[0].split('_')[1].lower()
            x, y, z = (float(line[2]), float(line[3]), float(line[4]))
            #print(pdb_id, x, y, z, is_hit(pdb_id, x, y, z))
            hit_index = is_hit(pdb_id, x, y, z)
            if hit_index == -1:
                actual_negatives += 1




def get_rates(target_specificity, hits_sorted_file):
    # returns index of point if corresponds to a gold standard hit, -1 otherwise

    with open(hits_sorted_file, "r") as f:
        lines = f.readlines()
        
        target_negatives = int((target_specificity * actual_negatives) // 1)
        num_neg = 0
        cutoff_ind = None
        i = len(lines)
        for line in lines[::-1]:
            i -= 1
            line = line.split("\t")
            pdb_id = line[0].split('_')[1].lower()
            x, y, z = (float(line[2]), float(line[3]), float(line[4]))
            #print(pdb_id, x, y, z, is_hit(pdb_id, x, y, z))
            hit_index = is_hit(pdb_id, x, y, z)
            if hit_index == -1:
                num_neg += 1
            if num_neg == target_negatives and not cutoff_ind:
                cutoff_ind = i
                break

        i = 0
        true_pos = 0
        false_pos = 0
        true_neg = 0
        false_neg = 0

        for line in lines:
            i += 1
            line = line.split("\t")
            pdb_id = line[0].split('_')[1].lower()
            x, y, z = (float(line[2]), float(line[3]), float(line[4]))
            
            hit = is_hit(pdb_id, x, y, z) >= 0

            if hit and i <= cutoff_ind:
                true_pos += 1
            if hit and i > cutoff_ind:
                false_neg += 1
            if not hit and i <= cutoff_ind:
                false_pos += 1
            if not hit and i > cutoff_ind:
                true_neg += 1
            
        assert(true_pos + false_pos + true_neg + false_neg)


        tp = true_pos / (true_pos + false_neg)
        fp = 1 - (true_neg / (true_neg + false_pos))
        return (tp, fp)


def calc_stats(hits_sorted_file, name):
    true_positives = []
    false_positives = []

    for fpr in range(1, 100, 5):
        tp, fp = get_rates(1 - fpr/100, hits_sorted_file)
        true_positives.append(tp)
        false_positives.append(fp)

    # area under the curve
    auc = np.trapz(true_positives, false_positives)

    plt.plot(false_positives, true_positives, linestyle='--', marker='o', color='darkorange', lw = 2, label='ROC curve', clip_on=False)
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve, AUC =' + str(auc))
    plt.legend(loc="lower right")
    plt.savefig(f'results/{name}.png')

    plt.clf()
    
    return (true_positives, false_positives, auc)

with open("results/res.csv", "w+") as f:
    for sub_dir in os.walk(OUT_DIR):
        dir_path = sub_dir[0]
        print(dir_path)
        name = dir_path.split("/")[-1].replace("-expr", "")
        if name == "out":
            # exclude the out directory
            continue
        # TODO remove, just used because we ran gauss previously
        if "-gauss" in name:
            continue
        num_shells, shell_width, num_bins, model_mode = tuple(name.split("-"))
        true_positives, false_positives, auc = calc_stats(f"{dir_path}/hits.sorted", name)
        
        f.write(f"{name}, {num_shells}, {shell_width}, {num_bins}, {model_mode}, {true_positives[0]}, {false_positives[0]}, {true_positives[2]}, {false_positives[2]}, {auc} \n")