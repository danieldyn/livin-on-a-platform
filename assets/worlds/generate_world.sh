#!/bin/bash

# Generate world template, containing
# 10 rows of sky blocks
# 44 rows of randomly generated dirt / underground blocks

row_len=72
sky_rows=20
ground_rows=34
target=$1

if [ $# -ne 1 ]; then
  echo "Usage: $0 <world_name>.txt"
  exit 1
fi

# Initialise file content
if [ -e "$target" ]; then
  rm $target
fi

touch $target

# Sky blocks
for i in $(seq 1 $sky_rows); do
  row=""
  for j in $(seq 1 $row_len); do
    row="${row}0"
  done
  echo $row >> $target
done

# Ground blocks
for i in $(seq 1 $ground_rows); do
  row=$(tr -dc '1gh' < /dev/urandom | head -c $row_len)
  echo $row >> $target
done

echo "Done creating $1"

