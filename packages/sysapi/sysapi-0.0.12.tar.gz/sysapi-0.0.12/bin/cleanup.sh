#!/bin/bash

POOL=$1
ROOTFS=$2

/bin/rm -rf /$ROOTFS/hf-1/*
/bin/rm -rf /$ROOTFS/lf-1/*
/bin/rm -rf /$ROOTFS/nobk-1/*
/bin/rm -rf /$ROOTFS/sync-1/*
/bin/rm -rf /$ROOTFS/System
/bin/rm -rf /$ROOTFS/etc/safer.pdb

for fs in `/sbin/zfs list -r -H -o name -t filesystem,volume $POOL`
do
    for snap in `/sbin/zfs list -H -t snapshot -o name $fs`
    do
	prop=`/sbin/zfs get inspeere.com:source -H -o value $snap`
	if [ "$prop" != "-" ]; then 
	    /sbin/zfs destroy $snap
	fi
    done
done
