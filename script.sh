#!/bin/bash

if [ $USER == marcos ]
then local_dir=repositorios
else local_dir=docs
fi

kern_dir=$HOME/$local_dir/genos-corpus/music/bach-chorales/kern
freq_dir=/tmp/freq

echo "Generating frequency lists..."

mkdir $freq_dir 2> /dev/null

for k in $(ls $kern_dir)
do
    n=${k%.krn}
    extractx -i '*Isoprn' $kern_dir/$k | \
        sed 's/[12468.JLX;]//g' | \
        freq | \
        rid -GLId | \
        egrep -v "=|r" | \
        uniq \
        > $freq_dir/$n.freq
done
