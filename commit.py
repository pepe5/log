#!/usr/bin/python
# for correct echoing needs $> reset
# for named sockets use script-name: dcomint
#>! dont send reset to maestro server - conman will not work

import os, pexpect, sys
l = ' '.join (sys.argv [2:])
dtach='dtach -A %s/tmp/\%s.dtach -z bash' % (os.environ['HOME'], sys.argv [1])

#(d) print "% -pcomint: " + dtach
p = pexpect.spawn (dtach)

#>? p.sendline ('')
#>? p.sendline ('echo ' + l) #>? "% #" 
print "\n%pcomint> " + l
p.sendline ('')
p.sendline (l)
p.sendline ('')
