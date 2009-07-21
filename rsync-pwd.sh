#!/bin/bash
# run it by watch '.../rsync-pwd.sh'
# if [$ARGC -ne 0]; then wd=$1; fi

pwd=`pwd`
rootFolder=`pwd | perl -ne '/(projects|tickets)\// and print "$1"'` # (?:projects)|(?:tickets)
prj=`basename "$pwd"`
rsync -av -e "ssh -l tester" ./ "jubiler:'$pwd'"
# rsync -av --exclude='.#*' ./ "/mnt/win/pepa/dox(!)/tasks/$rootFolder/$prj"

# rsync -av -e "ssh -l tester" ./ "jubiler:/home/tester/tst/kraljo/tickets/icr47292+i48736\ uP\ message\ archiving\ setting/"
