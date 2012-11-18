#!/usr/bin/env python

"""This spawns a sub-shell (bash) and gives the user interactive control. The
entire shell session is logged to a file called script.log. This behaves much
like the classic BSD command 'script'.

./script.py [-a] [-c command] {logfilename}

    logfilename : This is the name of the log file. Default is script.log.
    -a : Append to log file. Default is to overwrite log file.
    -c : spawn command. Default is to spawn the sh shell.

Example:

    This will start a bash shell and append to the log named my_session.log:

        ./script.py -a -c bash my_session.log

"""

import os, sys, time, getopt
import signal, fcntl, termios, struct
import traceback

#pep>
import time
sys.path.append('/home2/kraljo/opt/pexpect-2.3/')

import pexpect
global_pexpect_instance = None # Used by signal handler

def exit_with_usage():

    print globals()['__doc__']
    os._exit(1)

#pep>!- remove
class stopmarkC:
    stopmarkS = 0
stopmarkO = stopmarkC ()

def main():
    ######################################################################
    # Parse the options, arguments, get ready, etc.
    ######################################################################
    try:
        #pep> added 'lio'
        optlist, args = getopt.getopt(sys.argv[1:], 'h?ac:lio', ['help','h','?'])
    except Exception, e:
        print str(e)
        exit_with_usage()
    options = dict(optlist)
    if len(args) > 1:
        exit_with_usage()
        
    if [elem for elem in options if elem in ['-h','--h','-?','--?','--help']]:
        print "Help:"
        exit_with_usage()

    if len(args) == 1:
        script_filename = args[0]
    else:
        script_filename = "script.log"
    if '-a' in options:
        fout = file (script_filename, "ab")
    else:
        fout = file (script_filename, "wb")
    if '-c' in options:
        command = options['-c']
    else:
        command = "sh"

    # Begin log with date/time in the form CCCCyymm.hhmmss
    fout.write ('# %4d%02d%02d.%02d%02d%02d \n' % time.localtime()[:-3])
    
    ######################################################################
    # Start the interactive session
    ######################################################################
    p = pexpect.spawn(command)
    p.logfile = fout
    global global_pexpect_instance
    global_pexpect_instance = p
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)

    print "Script recording started."
    #>!  Type *?? ^] (ASCII 29) ??* to escape from the script shell.
    if '-l' in options:
        print 'pep> -log!'
        while 1:
            #>! p.logfile = sys.stdout
            l = p.read_nonblocking ()
            print '%s' % l,
            sys.stdout.flush ()
            i = raw_input ()
            print '> (%s)' % i
            # sys.stdout.flush ()
            p.sendline (i)
    elif '-i' in options:
        print 'pep> -in-filter!'
        uifout = file (script_filename + '.uistamped.log', "wb")
        def inf (data):
            uifout.write \
                ('\n>|%s|> %s\n' % \
                     (time.strftime ("%H:%M:%S", time.localtime()),
                      data)) #>? \n ?
            uifout.flush()
            return data
        def outf (data):
            uifout.write (data)
            # uifout.write \
            #     ('<(%s)< %s\n' % \
            #          (time.strftime ("%H:%M:%S", time.localtime()),
            #           data))
            uifout.flush()
            print "\n<<|("+ repr (stopmarkO.stopmarkS) +":"+ repr ("<pep>" in data) +")|" + data + "\n"
            if not ("<pep>" in data) and (stopmarkO.stopmarkS < 3):
                stopmarkO.stopmarkS += 1
                p.sendline ("date -Is #<pep>")
                
            #>? if not "<pep>" in data: p.sendline ("date -Is #<pep>")
            return data
        p.interact(chr(27), inf, outf) # 27 is ^[, 28 is ^\
    else:
        p.interact(chr(29)) # 29 is ^]

    fout.close()
    return 0

def sigwinch_passthrough (sig, data):

    # Check for buggy platforms (see pexpect.setwinsize()).
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912 # assume
    s = struct.pack ("HHHH", 0, 0, 0, 0)
    a = struct.unpack ('HHHH', fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ , s))
    global global_pexpect_instance
    global_pexpect_instance.setwinsize(a[0],a[1])

if __name__ == "__main__":
    try:
        main()
    except SystemExit, e:
        raise e
    except Exception, e:
        print "ERROR"
        print str(e)
        traceback.print_exc()
        os._exit(1)

