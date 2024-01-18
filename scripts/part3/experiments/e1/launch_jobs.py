import subprocess

# launch kubernetes jobs in for loop by running subprocesses
node_a_jobs = ["parsec-radix.yaml", "parsec-vips.yaml"]

for job in node_a_jobs:
    subprocess.run(["kubectl", "create", "-f", job])
    print("Launched job: ", job)

print("Launched all jobs")