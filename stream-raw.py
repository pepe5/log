#!/usr/bin/python
#>! http://stackoverflow.com/questions/3670323/setting-smaller-buffer-size-for-sys-stdin
#>? use p.send (), and for reading tail subprocess.communicate ()
#	http://stackoverflow.com/questions/8980050/persistent-python-subprocess

## usage:
#$ date -Is | cut -d+ -f1 > 123.out
#$ S=123.out; tail -f $S | while read L; do echo `date -Is | cut -d+ -f1`: -$S: $L; done &
#$ dtach -n 123.dtach -z script -f 123.in
#$ python -u ~/bin/stream-raw.py 123.in 123.out
#$ dtach -a 123.dtach #$ cat >> 123.helper
#
#>? tail -f 123.in | python ~/bin/stream-raw.py 123.out

import os, pexpect, shlex, subprocess, sys, time
tail = 'tail -f %s' % sys.argv [1] #>? (!) >> stdin
script = 'script -af /tmp/%s' % sys.argv [2]
print '%pcomint:> tail: ' + repr (shlex.split (tail))
#>? newin = os.fdopen (sys.stdin.fileno (), 'r', 0)
#	(vv) stdin = newin,

srcp = subprocess.Popen \
    (shlex.split (tail),
     bufsize = 0,
     stdout = subprocess.PIPE)
dstp = pexpect.spawn (script)

while 1:
    data = srcp.stdout.read (1)
    if data == '\x00':
        print '!' + data,
        data = srcp.stdout.readline () #! fixes dstp.send (data) :-S
    print '.' + data, # '\n%pcomint$> ' #(>) repr (data)
    dstp.send (data)

## OK:
# process = subprocess.Popen (['tail','-f', '/tmp/1.txt'], bufsize=1, stdout=subprocess.PIPE)
# while 1:
#     S = process.stdout.read (1)
#     print ".%s" % S,
