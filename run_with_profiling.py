import subprocess
import psutil
import sqlite3
from time import sleep


def run_with_profiling(command, list_of_arglists, sqlite_path='./profile.db', interval=1):
    """
    Run processes sequentially, recording process and memory usage to an sqlite database.

    :param command:
    Command to run
    :param list_of_arglists:
    A list of lists. Each element of the list should be a list of arguments to pass each time `command` is run.
    :param sqlite_path:
    Path to an sqlite database which will be filled with
    """
    for arglist in list_of_arglists:
        proc = subprocess.Popen([command, *arglist], stderr=subprocess.DEVNULL)
        psutil_process = psutil.Process(proc.pid)
        while proc.poll():
            sleep(1)
            print(psutil_process.memory_info())
