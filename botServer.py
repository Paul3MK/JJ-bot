import subprocess
import multiprocessing

myProcesses = ("actionServerRun.py", "dialogueServerRun.py")

def run_process(process):
    subprocess.Popen("python", "{}".format(process))

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=2)
    pool.map(run_process, myProcesses)
