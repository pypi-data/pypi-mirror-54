#!/bin/bash

POOL=$1
ROOTFS=$2

/bin/rm -rf /$ROOTFS/*


for fs in `/sbin/zfs list -r -H -o name -t filesystem,volume $ROOTFS`
do
    for snap in `/sbin/zfs list -H -t snapshot -o name $fs`
    do
	prop=`/sbin/zfs get inspeere.com:source -H -o value $snap`
	if [ "$prop" != "-" ]; then 
	    /sbin/zfs destroy $snap
	fi
    done
done
