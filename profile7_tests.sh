#! /bin/bash

population="-p 100"
epochs="-e 1000"
crossover_probability="-c 0.7"
mutation_probability="-m 0.01"
elite="-E 0.1"
jobs="-j 4"

# profile 7
file="data/blf/profile7"
resolution="-r 100 1"
out="-o profile7_res1001.png"
config="$file $out $population $epochs $crossover_probability $mutation_probability $elite $resolution $jobs"
echo $config
python blf_genetic/application.py $config > profile7_res1001.log

resolution="-r 50 1"
out="-o profile7_res501.png"
config="$file $out $population $epochs $crossover_probability $mutation_probability $elite $resolution $jobs"
echo $config
python blf_genetic/application.py $config > profile7_res501.log

resolution="-r 20 1"
out="-o profile7_res201.png"
config="$file $out $population $epochs $crossover_probability $mutation_probability $elite $resolution $jobs"
echo $config
python blf_genetic/application.py $config > profile7_res201.log

resolution="-r 10 1"
out="-o profile7_res101.png"
config="$file $out $population $epochs $crossover_probability $mutation_probability $elite $resolution $jobs"
echo $config
python blf_genetic/application.py $config > profile7_res101.log

