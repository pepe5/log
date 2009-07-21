# runs diff on parameter and moves .cursor 1 version back

from sys import *
from os import *
from re import *
from string import *

print 'running: ',
for i in argv: print i,
print

def main (argv):
    # print string.join (popen (r'show term') .readlines())
    # for i in file ('.cursor'): print i
    
    print 'making abs-path from argv1:',
    print 'dir /vers=1/nohead/notrail '+argv[-1]
    a = popen (r'dir /vers=1/nohead/notrail '+argv[-1]) \
        .readline() .strip() .split(';')
    
    print 'reading .cursor position: ',
    l = file ('.cursor') .readline() .strip() .split(';')
    print l
    print 'checking if .cursor is on that file...', 
    if l[0] <> a[0]:
        print '.cursor is not there! '
        print 'setting it... ',
        file ('.cursor','w') .write (';'.join(a))
        raise NameError, 'exiting.' # rather Warning?
    print 'ok.'
    
    print 'running: diff /para '+ ';'.join(l) # print int(l) - 1
    system ('diff /para '+ ';'.join(l))
    
    print 'decrement .cursor version to this one: ',
    l = "%s;%s" % ((l[0]), (int(l[-1]) -1))
    file ('.cursor','w') .write (l)
    print l # system ('type .cursor')

if __name__ == "__main__": main (argv[1:])
