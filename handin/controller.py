import psutil
import subprocess
import time
import docker
from docker.errors import NotFound
from scheduler_logger import SchedulerLogger, Job

radix = ("splash2x", "radix", "native")
blackscholes = ("parsec", "blackscholes", "native")
vips = ("parsec", "vips", "native")
ferret = ("parsec", "ferret", "native")
freqmine = ("parsec", "freqmine", "native")
canneal = ("parsec", "canneal", "native")
dedup = ("parsec", "dedup", "native")

#Changed order a bit due to sharing of LLC? Check about vips.
category1 = [dedup, radix, blackscholes]
category2 = [ferret, freqmine, canneal,vips]

mc_upper_lvl = 35   # here we switch to category 2
mc_lower_lvl = 45   # here we switch to category 1

class Category:
  def __init__(self, jobs):
    self.jobs = jobs
    self.current_job = -1
    self.done = False

def find_process_pid(process_name):
  for proc in psutil.process_iter(['pid', 'name']):
    if process_name in proc.info['name']:
      return proc.info['pid']
  return None

def set_mc_cores(pid, cores, logger):
  cmd = ["sudo", "taskset", "-a", "-cp", ", ".join(cores), str(pid)]
  try:
    subprocess.check_output(cmd)
    logger.update_cores(Job.MEMCACHED, cores)
    print("Taskset command executed successfully.")
  except subprocess.CalledProcessError as e:
    print("Error executing taskset command:", e)


def start_container(workload, category1, logger):
  client = docker.from_env()
  try:
    client.containers.run(
      "anakli/cca:" + workload[0] + "_" + workload[1],
      detach=True,
      cpuset_cpus="1" if category1 else "2-3",
      name=workload[1],
      command="./run -a run -S " + workload[0] + " -p " + workload[1] + \
          " -i native -n " + ("1" if category1 else "2")
    )
    logger.job_start(Job(workload[1]), ["1"] if category1 else ["2", "3"], \
                     1 if category1 else 2)
  except docker.errors.APIError as e:
    print("Error executing Docker command:", e)

def container_done(container_name, logger):
  client = docker.from_env()
  try:
    container = client.containers.get(container_name)
    if container.status == 'exited':
      logger.job_end(Job(container_name))
      return True
    else:
      return False
  except NotFound:
    print("Container " + container_name + " not found when checking if it's done")
    return False

def pause_container(container_name, logger):
  client = docker.from_env()
  try:
    container = client.containers.get(container_name)
    if container.status == 'running':
      container.pause()
      logger.job_pause(Job(container_name))
      return True
    elif container.status == 'exited':
      return True
    else:
      print(container.status)
      return False

  except NotFound:
    print("Container " + container_name + " not found when trying to pause")

def unpause_container(container_name, logger):
  client = docker.from_env()
  try:
    container = client.containers.get(container_name)
    if container.status == 'paused':
      container.unpause()
      logger.job_unpause(Job(container_name))
      return True
    elif container.status == 'exited':
      return True
    else:
      print(container.status)
      return False
    
  except NotFound:
    print("Container " + container_name + " not found when trying to unpause")

def pause_category1(category1, logger):
  if category1.done:
    return
  # first container not started yet -> nothing to pause
  if category1.current_job == -1:
    return
  while pause_container(category1.jobs[category1.current_job][1], logger) == False:
    #Just in case we switch from pause/unpause too quickly and docker status hasn't updated yet.
    print("Waiting for pause")
    time.sleep(0.2)

def unpause_category1(category1, logger):
  if category1.done:
    return
  # first container not started yet -> nothing to pause
  if category1.current_job == -1:
    return
  
  while unpause_container(category1.jobs[category1.current_job][1], logger) == False:
    #Just in case we switch from pause/unpause too quickly and docker status hasn't updated yet.
    print("Waiting for unpause")
    time.sleep(0.2)

def update_category1(category1, logger):
  if category1.done:
    return
  # start first container
  if category1.current_job == -1:
    category1.current_job += 1
    start_container(category1.jobs[category1.current_job], True, logger)
  elif container_done(category1.jobs[category1.current_job][1], logger):
    category1.current_job += 1
    if category1.current_job == len(category1.jobs):
      category1.done = True
    else:
      start_container(category1.jobs[category1.current_job], True, logger)

def update_category2(category2, logger):
  if category2.done:
    return
  # start first container
  if category2.current_job == -1:
    category2.current_job += 1
    start_container(category2.jobs[category2.current_job], False, logger)
  elif container_done(category2.jobs[category2.current_job][1], logger):
    category2.current_job += 1
    if category2.current_job == len(category2.jobs):
      category2.done = True
    else:
      start_container(category2.jobs[category2.current_job], False, logger)

def main():
  # initialize categories
  category1 = Category([dedup, radix, blackscholes])
  category2 = Category([ferret, freqmine, canneal,vips])

  # start logger
  logger = SchedulerLogger()

  # make sure memcached is currently running on 1 core and log the start
  mc_pid = find_process_pid("memcache")
  if not mc_pid:
    print("Didn't find the memcached process")
    return
  mc_proc = psutil.Process(mc_pid)
  set_mc_cores(mc_pid, ["0"], logger)
  logger.job_start(Job.MEMCACHED, ["0"], 2)
  mc_low = True

  while True:
    # check CPU usage of memcached
    mc_utilization = mc_proc.cpu_percent()
    
    if category1.done:
      if mc_low:
        set_mc_cores(mc_pid, ["0", "1"], logger)
        mc_low = False

    else:  
      if mc_low:
        if mc_utilization > mc_upper_lvl:
          pause_category1(category1, logger)
          set_mc_cores(mc_pid, ["0", "1"], logger)
          mc_low = False
        else:
          update_category1(category1, logger)
      else:
        if mc_utilization < mc_lower_lvl:
          set_mc_cores(mc_pid, ["0"], logger)
          unpause_category1(category1, logger)
          mc_low = True
          update_category1(category1, logger)

    update_category2(category2, logger)

    if category1.done and category2.done:
      logger.end()
      return
    elif category1.done:
      if category2.current_job < (len(category2.jobs) - 1):
        print("only category 1 done and still unscheduled category 2 jobs - \
              maybe implement scheduling of category 2 jobs on core 1?")
        
    elif category2.done:
      if category1.current_job < (len(category1.jobs) - 1):
        print("only category 2 done and still unscheduled category 1 jobs - \
              maybe implement scheduling of category 1 jobs on cores 2 and 3?")

    time.sleep(0.5)
    
if __name__ == "__main__":
  main()




