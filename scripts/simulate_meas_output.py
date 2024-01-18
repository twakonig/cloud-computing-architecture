import time


# sample data
header = ['#type', 'avg', 'std', 'min', 'p5', 'p10', 'p50', 'p67', 'p75', 'p80', 'p85', 'p90', 'p95', 'p99', 'p999', 'p9999', 'QPS', 'target']
out_1 = ['read', 446.9, 402.6, 160.7, 219.6, 240.4, 412.5, 494.8, 540.4, 573.7, 612.8, 663.7, 769.2, 962.6, 3367.1, 11130.9, 29739.4, 30000]
out_2 = ['read', 446.9, 402.6, 160.7, 219.6, 240.4, 412.5, 494.8, 540.4, 573.7, 612.8, 663.7, 665.2, 962.6, 3367.1, 11130.9, 34723.5, 35000]
out_3 = ['read', 446.9, 402.6, 160.7, 219.6, 240.4, 412.5, 494.8, 540.4, 573.7, 612.8, 663.7, 829.3, 962.6, 3367.1, 11130.9, 40031.4, 40000]
# read      442.2   251.3   160.7   221.2   242.2   410.8   489.1   534.9   568.9   610.1   664.8   771.5   956.9  2091.5  8970.5  34924.1    35000
# read      456.1   261.3   148.8   220.2   240.7   409.1   498.8   550.5   588.9   634.9   696.9   829.3  1219.0  2791.5  7716.2  40031.4    40000
output = [out_1, out_2, out_3]


def nice_print(row):
    '''print tab separated elments of a list'''

    msg = ''
    for i in range(len(row)):
        msg = msg + str(row[i]) + "\t"

    print(msg)
    return


def main():
    # simulate measurement outputs
    nice_print(header)
    
    for i in range(len(output)):
        time.sleep(0.1)
        nice_print(output[i])

    return


if __name__ == "__main__":
    main()