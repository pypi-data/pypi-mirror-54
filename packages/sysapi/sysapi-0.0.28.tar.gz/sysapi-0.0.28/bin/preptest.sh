#!/bin/bash

case $1 in
    test1)
    curl -X POST "http://192.168.1.45:8000/v1/snapshot/%40pre-joe" -H  "accept: application/json" || exit $?
    curl -X POST "http://192.168.1.45:8000/v1/users/new" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"username\":\"joe\",\"password\":\"string\",\"email\":\"user@example.com\",\"full_name\":\"string\"}" || exit $?
    curl -X POST "http://192.168.1.45:8000/v1/snapshot/%40post-joe" -H  "accept: application/json" || exit $?
    for i in 1 2 3 4 5
    do
        for dir in /srv/safer/home/joe/*
        do
            mkdir $dir/Rep$i
            touch $dir/$i
            touch $dir/Rep$i/$i
        done 
    done || exit $?
    curl -X POST "http://192.168.1.45:8000/v1/snapshot/%40post-joe-files" -H  "accept: application/json" | exit $?
    find /srv/safer/home/joe -exec chown www-data \{\} \;
    curl -X POST "http://192.168.1.45:8000/v1/snapshot/%40after-chown" -H  "accept: application/json" | exit $?
    ;;
esac

exit 0