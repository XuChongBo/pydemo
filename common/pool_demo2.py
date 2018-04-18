# coding=utf-8
from multiprocessing import Pool
import os, time, random
import subprocess, os, signal, sys

p = Pool(4) # 设置进程池大小
def long_time_task(name,other):
    try:
        print name
        print('Run task %s (%s) other %s...' % (name, os.getpid(), other))
        start = time.time()
        time.sleep(random.random() * 3)
        end = time.time()
        print('Task %s runs %0.2f seconds.' % (name, (end - start)))
    except KeyboardInterrupt:
        p.terminate()

def kill_child_processes(signum, frame):
    parent_id = os.getpid()
    ps_command = subprocess.Popen("ps -o pid --ppid %d --noheaders" % parent_id, shell=True, stdout=subprocess.PIPE)
    ps_output = ps_command.stdout.read()
    retcode = ps_command.wait()
    for pid_str in ps_output.strip().split("\n")[:-1]:
        os.kill(int(pid_str), signal.SIGTERM)
    sys.exit()


if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    for i in range(10):
        print("assgin:", i)
        p.apply_async(long_time_task, args=(i,i*2)) # 设置每个进程要执行的函数和参数
        # NOTE: 加了get(timeout)会导致串行
        #p.apply_async(long_time_task, args=(i,i*2)).get(1) # 设置每个进程要执行的函数和参数
        signal.signal(signal.SIGINT, kill_child_processes)
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
