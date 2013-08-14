#!/usr/bin/python
## TODO
#>! open io .dtach pipe outside of stream-raw.py -> you will be able to stop io w/o stopping session .dtach

## usage:
#$ T=$(basename `pwd`); H=$host1..
#$ echo $T: $H
#$ dtach -n $T.dtach -z script -f $T.in
#$ chmod -v 600 $T.in
#$ dtach -a $T.dtach
#$ cat >> $T.hist
#() nohup xterm -T $T -e dtach -a $T.dtach -z &

#() echo stream..py: -timestamp: `date -Is | cut -d+ -f1` > $H.out.log
#$ > $T.in; dtach -n $H.stream.dtach -z python -u ~/bin/stream-raw.py $T.in $H.dtach
#$ nohup xterm -xrm XTerm*ScrollBar:false -T $T:$H -e dtach -a $H.dtach -z &
#|| tail -f $H.out.log | while read L; do echo `date -Is | cut -d+ -f1`: -$H: $L; done &
#$ dtach -a $H.dtach
#$ script -af $H.out.log
#$ ssh .. $H


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
