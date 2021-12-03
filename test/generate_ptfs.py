import sys
import os.path


def main():
    if len(sys.argv) < 4:
        raise Exception("generate_ptfs.py requires <XXX.sites>, <XXX_sites.ptf>, and <XXX_nonsites.ptf> args")
    if not (os.path.isfile(sys.argv[1]) and sys.argv[1].endswith(".site")):
        raise Exception(f"input sites file arg doesn't end with .site: {sys.argv[1]}")
    with open(sys.argv[1]) as site_file, open(sys.argv[2], 'w') as pos_file, open(sys.argv[3], 'w') as neg_file:
        site_file.readline()
        for line in site_file:
            line_info = line.split()
            ptf_line_pref = f"{line[2:6]}\t{line_info[2]}\t{line_info[4]}\t{line_info[6]}\t"
            if line_info[7][0] == 'T':
                pos_file.write(f"{ptf_line_pref}site\n")
            else:
                neg_file.write(f"{ptf_line_pref}nonsite\n")


if __name__ == "__main__":
    main()
