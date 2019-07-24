#### Custom queueing script
#### usage: EGGtimer.py x y
#### x = absolute path to directory containing bash scripts to be queued
#### y = number of parallel subprocesses to spawn

import subprocess as sub
import os
import time
import sys

path_queue = sys.argv[1]
maxprocesses = int(sys.argv[2])

proclist = []
runningprocesses = 0
queue = [path_queue + x for x in os.listdir(path_queue)]

sys.stdout.write('found a total of {} scripts in folder {}\n'.format(len(queue), path_queue))
while True:
    sys.stdout.write('{} processes currently running!\n'.format(len(proclist)))
    if proclist:
        procstoremove = []
        for i, p in enumerate(proclist):
            if p.poll() == 0:
                sys.stdout.write('deleting proc {}\n'.format(p.pid))
                procstoremove.append(i)
        for number in procstoremove:
            del proclist[number]

    if len(proclist) < maxprocesses:
        try:
            currenttask = queue.pop()
        except IndexError:
            sys.stdout.write('queue empty!\n')
            if not proclist:
                sys.stdout.write('proclist empty!\n')
                break
        else:
            sys.stdout.write('starting to process script {}\n'.format(currenttask))
            proclist.append(sub.Popen([currenttask]))
            sys.stdout.write('new process {} started!\n'.format(proclist[-1].pid))
            #print [x.pid for x in proclist]
            #print [x.poll() for x in proclist]
    time.sleep(1)
print 'FINISHED'