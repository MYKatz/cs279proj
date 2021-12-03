"""

Compare with gold standard

1. Parse gold standard site file, create list of gold standard points
2. Mark each line in output as either gold-standard positive or negative
3. Go down the array until you hit a sensitivity of 99%
4. (later) graph the ROC curve

"""

GOLD_STANDARD_SITE = "/home/katz/Code/cs279proj/eval/calciums.CA.site"
# hits file, sorted from highest score (most likely to be a hit) to lowest
HITS_SORTED_FILE = "/home/katz/Code/cs279proj/out/6-1.25-5-nongauss/hits-r.sorted"

HIT_ANGSTROM_MAX_DISTANCE = 2

# dict of pdb id: [list of gold standard sites (3-tuples)]
gold = {}

# returns true if corresponds to a gold standard hit
def is_hit(pdb_id, x, y, z):
    true_positives = gold[pdb_id]
    for point in true_positives:
        dist = ((point[0] - x)**2 + (point[1] - y)**2 + (point[2]-z)**2)**0.5
        if dist < HIT_ANGSTROM_MAX_DISTANCE:
            return True
    return False

with open(GOLD_STANDARD_SITE, "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.split(" ")
        pdb_id = line[0].split('"')[1].lower()
        x, y, z = (float(line[2]), float(line[4]), float(line[6]))
        
        if pdb_id not in gold:
            gold[pdb_id] = []
        gold[pdb_id].append((x, y, z))


with open(HITS_SORTED_FILE, "r") as f:
    lines = f.readlines()
    for line in lines[:20]:
        line = line.split("\t")
        pdb_id = line[0].split('_')[1].lower()
        x, y, z = (float(line[2]), float(line[3]), float(line[4]))
        print(pdb_id, x, y, z, is_hit(pdb_id, x, y, z))
