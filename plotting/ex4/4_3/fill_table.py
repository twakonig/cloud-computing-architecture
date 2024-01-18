import numpy as np

# script to fill table in report with mean execution time *without* pauses, and standard deviation
# outputs start times, end times and execution times
# uses the processed logs (log_1_processed.txt, log_2_processed.txt, log_3_processed.txt)


directory = "data/"

def main():
    processed_logs = ["log_1_processed.txt", "log_2_processed.txt", "log_3_processed.txt"]
    t_exec_all = []
    t_start_all = []
    t_end_all = []
    for log in processed_logs:
        t_exec_i = []
        job_order = []
        t_start_run = []
        t_end_run = []
        filename = directory + log

        with open(filename, 'r') as f:
            line = f.readline()
            while line:
                # process line
                job_details = line.split(', ')
                t_start = job_details[1].split(':')
                t_end = job_details[2].split(':')
                pause = float(job_details[3].split('\n')[0])

                # start and end time in seconds
                t_start = 3600 * int(t_start[0]) + 60 * int(t_start[1]) + float(t_start[2])
                t_end = 3600 * int(t_end[0]) + 60 * int(t_end[1]) + float(t_end[2])
                t_start_run.append(t_start)
                t_end_run.append(t_end)

                # compute total execution time in seconds
                t_exec = round((t_end - t_start - pause), 2)
                t_exec_i.append(t_exec)

                # see which numbre corresponds to which job
                job_order.append(job_details[0])

                # read next line
                line = f.readline()

        t_exec_all.append(t_exec_i)
        t_start_all.append(t_start_run)
        t_end_all.append(t_end_run)


    print('jobs: ', job_order)

    # declare numpy arrays and transpose (jobs are per row)
    t_exec_all = np.array(t_exec_all)
    t_exec_all = np.transpose(t_exec_all)
    t_start_all = np.array(t_start_all)
    t_start_all = np.transpose(t_start_all)
    t_end_all = np.array(t_end_all)
    t_end_all = np.transpose(t_end_all)

    # get row wise mean and standard deviation
    t_exec_mean = np.mean(t_exec_all, axis=1)
    t_exec_std = np.std(t_exec_all, axis=1)

    # TODO: UNCOMMENT TO FILL TABLE
    print('mean time: \n', np.around(t_exec_mean, 2))
    print('std: \n', np.around(t_exec_std, 2))

    # print('start times: \n', np.around(t_start_all, 2))
    # print('end times: \n', np.around(t_end_all))
    # print('execution time (pause time subtracted): \n', np.around(t_exec_all, 2))


    return job_order, np.around(t_start_all, 2), np.around(t_end_all, 2), np.around(t_exec_all, 2)

   
if __name__ == "__main__":
    main()
