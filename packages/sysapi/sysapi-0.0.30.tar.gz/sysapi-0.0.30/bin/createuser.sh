#!/bin/bash

## $1 = login
## $2 = password
## $3 = email
## $4 = full name


/bin/echo "Creating user..."
for p in "$@"
do
    /bin/echo "Param: $p"
done

