import os

directory = f"/home/katz/Code/cs279proj/pdbs/calcium/dssp"

for filename in os.listdir(directory):
    name = filename.replace("pdb", "dssp")
    os.system(f"dssp {filename} > {name}")
    