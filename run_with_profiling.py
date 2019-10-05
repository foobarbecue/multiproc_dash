import subprocess
import psutil
import sqlite3
import pandas
from time import sleep


def run_with_profiling(command, list_of_arglists, sqlite_path='./profile.db', interval=5):
    """
    Run processes sequentially, recording process and memory usage to an sqlite database.

    :param command:
    Command to run
    :param list_of_arglists:
    A list of lists. Each element of the list should be a list of arguments to pass each time `command` is run.
    :param sqlite_path:
    Path to an sqlite database which will be filled with performance info
    """
    db_conn = sqlite3.connect(sqlite_path)
    for arglist in list_of_arglists:
        # proc = subprocess.Popen([command, *arglist], stderr=subprocess.DEVNULL)
        proc = subprocess.Popen([command, *arglist])
        psutil_process = psutil.Process(proc.pid)
        while not proc.poll():
            sleep(interval)
            now = pandas.datetime.now()
            with psutil_process.oneshot():
                df = pandas.DataFrame(columns=('cmd', 'args', 'CPU', 'mem')).astype({'CPU': float, 'mem': int})
                cpu_perc = psutil_process.cpu_percent()
                mem = psutil_process.memory_info().rss
                df.loc[now, :] = [command, ' '.join(arglist), cpu_perc, mem]
                df.to_sql('proc_prof', db_conn, if_exists='append')
