#!/usr/bin/python
## TODO
#>! open io .dtach pipe outside of stream-raw.py -> you will be able to stop io w/o stopping session .dtach

## usage:
#$ for H in host1 host2 ..; do logx $H; done
#$ for F in *stream.dtach; do dtach -a $F; done
#? kill -INT `pgrep -f '^python.*$H'`
#$ kill -INT `pgrep -f 'dtach -n $H'`

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
