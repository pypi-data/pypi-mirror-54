'''
Created on 26 Jan 2018

@author: Martin Franckie

Module for handling interactions with the system, such as running external
programs.
'''

from subprocess import call, Popen, PIPE
import os
import time
import aftershoq.utils.debug as dbg
from tempfile import TemporaryFile as tmp

def mkdir(name):
    '''Make directory "name", recursively.'''

    try:
        os.makedirs(name)
    except OSError:
        print("WARNING: Could not create directory " + name + "!")

def rmdir(name):
    '''Delete directory "name". Calls rm.'''

    os.removedirs(name)

def ls(path = "."):
    '''List files and directories in path. Calls ls.'''

    return os.listdir(path)

def listdirs(path):
    '''List directories only in path.'''
    output = []
    [output.append(d) for d in os.listdir(path) if os.path.isdir(path+"/"+d)]

    return output

def abspath(path):
    '''Returns absolute path of input path.'''
    wd = os.getcwd()
    os.chdir(path)
    abspath = os.getcwd()
    os.chdir(wd)

    return abspath


def waitforproc(proc,delay = 0.1):
    '''Wait for the process proc to finish. Sleep with delay seconds.'''
    while proc.poll() == None:
        time.sleep()

def dispatch(prog,args,dirpath=None, infile = None, outfile = None, errfile = None):
    '''Dispatch program prog with arguments args.

    Optional parameters:
    dirpath: Path to working directory.
    infile:  File with inputs to the program. Use subprocess.PIPE for input stream.
    outfile: File for program output. Use subprocess.PIPE for output stream.
    errfile: File for program output. Use subprocess.PIPE for output stream.

    Returns the Popen() process.

    Note that if all outputs are piped, the system can cause the program to crash
    since the pipes might not be properly closed between calls.
    '''

    if infile is None:
        infile = tmp()
    if outfile is None:
        outfile = tmp()
    if errfile is None:
        errfile = tmp()

    if args == []:
        progargs = prog
    else:
        progargs = [prog]

        for a in args:
            progargs.append(a)

    if dirpath is None:
        dirpath = "./"

    dbg.debug( "<<<< Dispatching program: " + str(progargs) + " from " + dirpath,
               dbg.verb_modes["chatty"])

    process=Popen(progargs,cwd=dirpath,close_fds=True,stdout=outfile,stderr=errfile,stdin=infile,
                  universal_newlines=True)

    dbg.debug(  " with pid="+str(process.pid)+" >>>>\n" ,
                dbg.verb_modes["chatty"])
    dbg.flush()
    return process
