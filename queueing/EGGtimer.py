#### Custom queueing script
#### usage: EGGtimer.py x y
#### x = absolute path to directory containing bash scripts to be queued
#### y = number of parallel subprocesses to spawn

import subprocess as sub
import os
import time
import sys

path_queue = sys.argv[1]
maxprocesses = sys.argv[2]

proclist = []
runningprocesses = 0
queue = [path_queue + x for x in os.listdir(path_queue)]

sys.stdout.write('found a total of {} scripts in folder {}\n'.format(len(queue), path_queue))
while True:
    sys.stdout.write('{} processes currently running!'.format(len(proclist)))
    if proclist:
        procstoremove = []
        for i, p in enumerate(proclist):
            if p.poll() == 0:
                print 'deleting proc {}'.format(p.pid)
                procstoremove.append(i)
        for number in procstoremove:
            del proclist[number]

    if len(proclist) <= 5:
        try:
            currenttask = queue.pop()
        except IndexError:
            print 'queue empty!'
            if not proclist:
                print 'proclist empty!'
                break
        else:
            sys.stdout.write('starting to process script {}'.format(currenttask))
            proclist.append(sub.Popen([currenttask]))
            print [x.pid for x in proclist]
            print [x.poll() for x in proclist]
    time.sleep(1)
print 'FINISHED'