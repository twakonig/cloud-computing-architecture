import psutil
import time

def main():
  mc_pid = 0
  for proc in psutil.process_iter(['pid', 'name']):
    if "memcache" in proc.info['name']:
      mc_pid = proc.info['pid']
  print("memcached process id:", mc_pid)
  mc_proc = psutil.Process(mc_pid)

  while True:
    mc_utilization = mc_proc.cpu_percent()
    print(int(time.time()), mc_utilization)
    time.sleep(0.5)

if __name__ == "__main__":
  main()
