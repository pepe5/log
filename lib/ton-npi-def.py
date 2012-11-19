from os import *
from re import * 

for i in file ("smsc$root:[srcref]fcdr.ry") .readlines ():
  if match (r'typeofnumb',i,I): p=1
  if match (r'NumberingPlanIn',i,I): p=1
  if match (r'.*0\.\.255',i,I):
    if p: print i,
    p=None
  if p: print i,
