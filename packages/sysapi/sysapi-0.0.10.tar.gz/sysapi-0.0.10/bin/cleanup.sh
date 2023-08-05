#!/bin/bash

POOL=$1
ROOTFS=$2

/bin/rm -rf /$ROOTFS/hf-1/*
/bin/rm -rf /$ROOTFS/lf-1/*
/bin/rm -rf /$ROOTFS/nobk-1/*
/bin/rm -rf /$ROOTFS/sync-1/*
/bin/rm -rf /$ROOTFS/System
/bin/rm -rf /$ROOTFS/etc/safer.pdb

for fs in `zfs list -r -H -o name -t filesystem,volume $POOL`
do
    for snap in `/sbin/zfs list -H -t snapshot -o name $fs`
    do
	prop=`zfs get inspeere.com:autogen -H -o value $snap`
	if [ "$prop" == "yes" ]; then 
	    zfs destroy $snap
	fi
    done
done
