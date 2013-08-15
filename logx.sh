#!/bin/bash

H=$1
T=$(basename `pwd`);
echo -$T:$H

> $T.in; dtach -n $H.stream.dtach -z python -u stream-raw.py $T.in $H.dtach
sleep 1; commit.py $H script -af $H.out.log
sleep 1; xterm -xrm XTerm*ScrollBar:false -T $T:$H -e dtach -a $H.dtach -z &
sleep 1; commit.py $H ". lk; slsssh root@$H"

#>? nohup
