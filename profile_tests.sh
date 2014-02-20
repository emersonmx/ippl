#! /bin/bash

default="-p 20 -e 500 -c 1.0 -E 0.1 -j 5"

# profile 7
basename="profile7"
file="data/blf/$basename"
out="-o $basename"
config="$file $out $default"
echo $config
python blf_genetic/application.py $config > $basename.log

# profile 8
basename="profile8"
file="data/blf/$basename"
out="-o $basename"
config="$file $out $default"
echo $config
python blf_genetic/application.py $config > $basename.log

# profile 6
basename="profile6"
file="data/blf/$basename"
out="-o $basename"
config="$file $out $default"
echo $config
python blf_genetic/application.py $config > $basename.log

# profile 9
basename="profile9"
file="data/blf/$basename"
out="-o $basename"
config="$file $out $default"
echo $config
python blf_genetic/application.py $config > $basename.log

#profile 10
basename="profile10"
file="data/blf/$basename"
out="-o $basename"
config="$file $out $default"
echo $config
python blf_genetic/application.py $config > $basename.log

