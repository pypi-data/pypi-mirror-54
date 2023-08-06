import os
import subprocess


def get_process_id(name):
    child = subprocess.Popen(["pgrep", "-f", name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    response = response.decode("utf-8")
    return response


def kill_process(name):
    pid = get_process_id(name)
    # print(pid)
    pidlist = pid.split("\n")
    for i in range(len(pidlist)):
        os.system("sudo kill -s  9 " + pidlist[i])
