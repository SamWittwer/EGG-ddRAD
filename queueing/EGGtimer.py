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
        if proclist:
            # if there are one or more processes running, check if any of them have finished and add to list
            procstoremove = []
            for i, p in enumerate(proclist):
                if p.poll() == 0:
                    logfile.write('{} - proc {} is finished!\n'.format(datetime.datetime.now(), p.pid))


            # if there are finished processes, kick them out of the running process list
            try:
                proclist = [x for x in proclist if x != None]
            except ValueError:
                pass

        if len(proclist) < maxprocesses:
            # if len(list of processes) is below the max, spawn a new subprocess
            try:
                # see if there are tasks left in the queue
                currenttask = queue.pop()
            except IndexError:
                # queue is empty, wait 5 min before checking again
                logfile.write('{} - queue empty!\n'.format(datetime.datetime.now()))
                if not proclist:
                    # all processes killed or deleted, break out of while loop and end
                    logfile.write('{} - proclist empty!\n'.format(datetime.datetime.now()))
                    break
                time.sleep(299)
            else:
                # there was a process in queue, spawn a new process with this
                logfile.write('{} - starting to process script {}\n'.format(datetime.datetime.now(), currenttask))
                proclist.append(sub.Popen([currenttask]))
                logfile.write('{} - new process {} started!\n'.format(datetime.datetime.now(), proclist[-1].pid))

        # execute while loop every second to check for finished processes
        time.sleep(1)

    # program finishes, finalize log file
    logfile.write('{} - FINISHED'.format(datetime.datetime.now()))