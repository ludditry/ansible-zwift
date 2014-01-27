#!/bin/bash

#
# Info:
#   There may be occasions when the swift drive audit will not 
#   pickup on devices that are having issues due to XFS corruption.
#   This scrip, called from a cronjob, will send an alert to the email
#   provided if XFS corruption has been found.
#

TMPF=`mktemp`
KERNLOG="/var/log/kern.log"

HOST=$(hostname  -f | cut -d "." -f1,2)
STARTTIME=$(date +"%b %e %T")
ENDTIME=$(date -d "-10 minutes"  +"%b %_d %T")

EMAILS="swiftops"

LOCKFILE="/tmp/.xfs_corruption_check"
if [ -e $LOCKFILE ]; then
        exit 1
else
        touch $LOCKFILE
fi

awk '$0>=from&&$0<=to' from="$ENDTIME" to="$STARTTIME" $KERNLOG | cut -d "]" -f 2 | grep "Corruption detected" | uniq > $TMPF

test -s $TMPF
if [ $? -eq 0 ]; then
        MAILTMP=`mktemp`

        msg="\n"
        msg=${msg}"\n An XFS corruption was found on this system"
        msg=${msg}"\n Please check on device filesystem"
        msg=${msg}"\n It's up to you if you want to xfs_repair (long run)"
        msg=${msg}"\n the device or just re-create the File System\n\n"

        echo -e ${msg} > $MAILTMP
        cat $TMPF >> $MAILTMP
        cat $MAILTMP | mail -s "XFS Corruption detected on $HOST ($ENDTIME - $STARTTIME)" $EMAILS
        rm -f $MAILTMP
fi

rm -f $TMPF
rm -f $LOCKFILE
exit 0

