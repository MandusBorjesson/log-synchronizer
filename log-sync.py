#!/usr/bin/python3

import sys
from datetime import datetime

def print_help():
    print(f'Usage: {sys.argv[0]} log1.txt format1 log2.txt format2 ...')
    print('')
    print(f'Example: {sys.argv[0]} test.txt "%b %d %H:%M:%S"')

def read_files(files):
    master = {}

    fmt_err = ' does not match format '
    exp_err = 'unconverted data remains: '

    for i in range(0, len(files), 2):
        name = files[i]
        t_format = files[i+1]
        f_index = int(i/2)

        with open(name, 'r') as f:
            time = datetime(1, 1, 1, 0, 0)
            lines = f.readlines()
            for l in lines:
                line = ''
                # Since strptime cant handle getting the time from part of a
                # string, attempt to get it and extrapolate the string and time
                # from the raised exception.
                try:
                    time = datetime.strptime(l, t_format)
                except ValueError as e:
                    if exp_err in str(e):
                        line = str(e).split(exp_err)[1]
                        time = datetime.strptime(l.split(line)[0], t_format)
                    elif fmt_err in str(e):
                        line = l
                        print(f'E: line does not match format, appending to last timestamp. ("{t_format}" / "{line.strip()}"')
                    else:
                        raise

                # Add line to master dictionary hierarchy is as follows:
                # timestamp_0
                #   file_index_0
                #     [line_0, line_1, ...]
                #   file_index_1
                #     [line_0, line_1, ...]
                # timestamp_1
                #   file_index_1
                #     [line_0, line_1, ...]
                # ...
                # timestamp_N
                #   f_index_0
                #     [line_0, line_1, ...]

                line = line.strip()
                if time in master:
                    if f_index in master[time]:
                        master[time][f_index].append(line)
                    else:
                        master[time][f_index] = [line]
                else:
                    master[time] = dict([(f_index, [line])])

    for d in sorted(master):
        print(d)
        for f in master[d]:
            print(f'  {f}')
            for l in master[d][f]:
                print(f'    {l}')

if __name__ == "__main__":
    if '-h' in sys.argv or '--help' in sys.argv:
        print_help()
        exit(0)

    if len(sys.argv) == 1:
        print_help()
        exit(1)

    if (len(sys.argv)+1)%2 != 0:
        print_help()
        exit(1)

    read_files(sys.argv[1:])
