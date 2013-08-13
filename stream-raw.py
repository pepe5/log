#!/usr/bin/python
#>! http://stackoverflow.com/questions/3670323/setting-smaller-buffer-size-for-sys-stdin
#>? use p.send (), and for reading tail subprocess.communicate ()
#	http://stackoverflow.com/questions/8980050/persistent-python-subprocess

## usage:
#$ T=$(basename `pwd`); H1=$host1..
#$ echo stream..py: -timestamp: `date -Is | cut -d+ -f1` > $H1.out.log
#$ tail -f $H1.out.log | while read L; do echo `date -Is | cut -d+ -f1`: -$H1: $L; done &
#$ dtach -n $T.dtach -z script -f $T.in

#$ > $T.in; dtach -n $H1.stream.dtach -z python -u ~/bin/stream-raw.py $T.in $H1.dtach
#$ dtach -a $H1.dtach
#$ script -af $H1.out.log

#$ dtach -a $T.dtach
#? stty -echo
#$ cat >> $T.hist

import os, pexpect, shlex, subprocess, sys, time
inputter = 'tail -f %s' % sys.argv [1] #>? (!) >> stdin
outputter = 'dtach -A %s -z bash' % sys.argv [2]
#>! make dtach-startup starting $> script -af %s

print '%pcomint:> outputter: ' + repr (shlex.split (outputter))
#>? newin = os.fdopen (sys.stdin.fileno (), 'r', 0)
#	(vv) stdin = newin,

inp = subprocess.Popen \
    (shlex.split (inputter),
     bufsize = 0,
     stdout = subprocess.PIPE)
outp = pexpect.spawn (outputter)

while 1:
    data = inp.stdout.read (1)
    if data == '\x00':
        print '!' + data,
        data = inp.stdout.readline () #! fixes outp.send (data) :-S
    print '.' + data, # '\n%pcomint$> ' #(>) repr (data)
    outp.send (data)

## OK:
# process = subprocess.Popen (['tail','-f', '/tmp/1.txt'], bufsize=1, stdout=subprocess.PIPE)
# while 1:
#     S = process.stdout.read (1)
#     print ".%s" % S,
