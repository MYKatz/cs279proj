import sys
import os.path


def main():
    if len(sys.argv) < 4:
        raise Exception("generate_ptfs.py requires <XXX_sites.ptf>, <XXX_nonsites.ptf> and <XXX.sites> args")
    pos_file = open(sys.argv[1], 'w')
    neg_file = open(sys.argv[2], 'w')
    for site_file_dir in sys.argv[3:]:
        if not (os.path.isfile(site_file_dir) and site_file_dir.endswith(".site")):
            raise Exception(f"input sites file arg doesn't end with .site: {site_file_dir}")
        with open(site_file_dir) as site_file:
            site_file.readline()
            for line in site_file:
                if line == ")))\n":
                    break
                line_info = line.split()
                ptf_line_pref = f"{line[2:6]}\t{line_info[2]}\t{line_info[4]}\t{line_info[6]}\t"
                if line_info[7][0] == 'T':
                    pos_file.write(f"{ptf_line_pref}site\n")
                else:
                    neg_file.write(f"{ptf_line_pref}nonsite\n")
    pos_file.close()
    neg_file.close()


if __name__ == "__main__":
    main()
