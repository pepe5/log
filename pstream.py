#!/usr/bin/python
## usage:
# [tmp]$ tail -f prj123.script &
# [tmp]$ dtach -n prj123.dtach -z script -af prj123.script
# [tmp]$ stream.py prj123 <<EOF

import os, pexpect, sys, time
# dtach='dtach -A %s/tmp/\%s.dtach -z bash' % (os.environ['HOME'], sys.argv [1])
dtach='dtach -a %s/tmp/%s.dtach -z' % (os.environ['HOME'], sys.argv [1])
print '%pcomint> dtach: ' + dtach
p = pexpect.spawn (dtach)
while 1:
    l = sys.stdin.readline ()
    if not l:
        print '\n%pcomint> break.' + l
        break
    l = l.rstrip ()
    if len (l) < 1:
        print '\n%pcomint> next.' + l
        next
    if l.startswith ('/'):
        print '\n%pcomint/> ' + l
        time.sleep (int (l.split (' ') [1]))
    else:
        print '\n%pcomint$> ' + l
        p.sendline (l)
