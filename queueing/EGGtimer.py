#### Custom queueing script
#### usage: EGGtimer.py x y
#### x = absolute path to directory containing bash scripts to be queued
#### y = number of parallel subprocesses to spawn

import subprocess as sub
import os
import time
import sys
import datetime

path_queue = sys.argv[1]
maxprocesses = int(sys.argv[2])


proclist = []
runningprocesses = 0
queue = [path_queue + x for x in os.listdir(path_queue)]


with open('queuelog.txt', 'a') as logfile:
    logfile.write('{} - found a total of {} scripts in folder {}\n'.format(datetime.datetime.now(), queue, path_queue))
    while True:
        logfile.write('{} - {} processes currently running!\n'.format(datetime.datetime.now(), len(proclist)))
        if proclist:
            procstoremove = []
            for i, p in enumerate(proclist):
                if p.poll() == 0:
                    logfile.write('{} - deleting proc {}\n'.format(datetime.datetime.now(), p.pid))
                    procstoremove.append(i)
            for number in procstoremove:
                del proclist[number]

        if len(proclist) < maxprocesses:
            try:
                currenttask = queue.pop()
            except IndexError:
                logfile.write('{} - queue empty!\n'.format(datetime.datetime.now()))
                if not proclist:
                    logfile.write('{} - proclist empty!\n'.format(datetime.datetime.now()))
                    break
            else:
                logfile.write('{} - starting to process script {}\n'.format(datetime.datetime.now(), currenttask))
                proclist.append(sub.Popen([currenttask]))
                logfile.write('{} - new process {} started!\n'.format(datetime.datetime.now(), proclist[-1].pid))
                #print [x.pid for x in proclist]
                #print [x.poll() for x in proclist]
        time.sleep(1)
    logfile.write('{} - FINISHED'.format(datetime.datetime.now()))