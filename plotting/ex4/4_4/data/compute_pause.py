import sys
import numpy as np


def main(argv):
    # get file with two rows: pause times & corresponding unpause times
    filename = argv[0]

    # read two lines of txt file into two arrays, delimited by ,
    with open(filename, 'r') as f:
        start_p = f.readline().split(', ')[:-1]
        end_p = f.readline().split(', ')[:-1]

    # convert to seconds
    for i in range(len(start_p)):
        start_p_i = start_p[i].split(':')
        start_p[i] = 3600 * int(start_p_i[0]) + 60 * int(start_p_i[1]) + float(start_p_i[2])
        
    for i in range(len(end_p)):
        end_p_i = end_p[i].split(':')
        end_p[i] = 3600 * int(end_p_i[0]) + 60 * int(end_p_i[1]) + float(end_p_i[2])

    # convert to numpy arrays
    start_p = np.array(start_p)
    end_p = np.array(end_p)
    if start_p.shape != end_p.shape:
        start_p = start_p[:-1]

    # compute pause times
    pauses_vec = end_p - start_p
    total_pause = round(np.sum(pauses_vec), 2)
    print(total_pause)
    return total_pause

if __name__ == "__main__":
    main(sys.argv[1:])



