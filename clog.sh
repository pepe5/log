#!/bin/bash

H=$1
T=$(basename `pwd`);
echo -$T:$H

if ! [ -f $T.dtach ]; then
    dtach -n $T.dtach -z script -f $T.in; chmod -v 600 $T.in
    sleep 1; commit.py $T "reset; cat >> $T.hist"
    sleep 4 #>? ; commit.py $T script -af $T.in
fi

> $T.in; dtach -n $H.stream.dtach -z stream-raw.py $T.in $H.dtach
sleep 1; commit.py $H script -af $H.out.log
sleep 1; xterm -xrm XTerm*ScrollBar:false -T $T:$H -e dtach -a $H.dtach -z &
sleep 1; commit.py $H ". lk; slsssh root@$H"

#() nohup xterm -T $T -e dtach -a $T.dtach -z &
#() echo stream..py: -timestamp: `date -Is | cut -d+ -f1` > $H.out.log
#|| tail -f $H.out.log | while read L; do echo `date -Is | cut -d+ -f1`: -$H: $L; done &
#() dtach -a $H.dtach
