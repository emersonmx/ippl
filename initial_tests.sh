#! /bin/bash

file="data/blf/profile7"
population="--population 1000"
epochs="--epochs 1000"
crossover_probability="--crossover_probability 1"
elite="--elite 0.1"
jobs="--jobs 4"

resolution="--resolution 100 1"
out="--out test_res1001.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > test_res1001.log

resolution="--resolution 50 1"
out="--out test_res501.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > test_res501.log

resolution="--resolution 20 1"
out="--out test_res201.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > test_res201.log

resolution="--resolution 10 1"
out="--out test_res101.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > test_res101.log

resolution="--resolution 5 1"
out="--out test_res51.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > test_res51.log

resolution="--resolution 1 1"
out="--out test_res11.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > test_res11.log

