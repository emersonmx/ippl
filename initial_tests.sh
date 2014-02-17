#! /bin/bash

population="--population 1000"
epochs="--epochs 1000"
crossover_probability="--crossover_probability 1"
elite="--elite 0.1"
jobs="--jobs 4"

# profile 6
file="data/blf/profile6"
resolution="--resolution 100 1"
out="--out profile6_res1001.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile6_res1001.log

resolution="--resolution 50 1"
out="--out profile6_res501.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile6_res501.log

resolution="--resolution 20 1"
out="--out profile6_res201.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile6_res201.log

resolution="--resolution 10 1"
out="--out profile6_res101.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile6_res101.log

resolution="--resolution 5 1"
out="--out profile6_res51.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile6_res51.log

resolution="--resolution 1 1"
out="--out profile6_res11.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile6_res11.log

# profile 7
file="data/blf/profile7"
resolution="--resolution 100 1"
out="--out profile7_res1001.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile7_res1001.log

resolution="--resolution 50 1"
out="--out profile7_res501.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile7_res501.log

resolution="--resolution 20 1"
out="--out profile7_res201.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile7_res201.log

resolution="--resolution 10 1"
out="--out profile7_res101.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile7_res101.log

resolution="--resolution 5 1"
out="--out profile7_res51.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile7_res51.log

resolution="--resolution 1 1"
out="--out profile7_res11.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile7_res11.log

# profile 8
file="data/blf/profile8"
resolution="--resolution 100 1"
out="--out profile8_res1001.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile8_res1001.log

resolution="--resolution 50 1"
out="--out profile8_res501.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile8_res501.log

resolution="--resolution 20 1"
out="--out profile8_res201.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile8_res201.log

resolution="--resolution 10 1"
out="--out profile8_res101.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile8_res101.log

resolution="--resolution 5 1"
out="--out profile8_res51.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile8_res51.log

resolution="--resolution 1 1"
out="--out profile8_res11.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile8_res11.log

# profile 9
file="data/blf/profile9"
resolution="--resolution 100 1"
out="--out profile9_res1001.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile9_res1001.log

resolution="--resolution 50 1"
out="--out profile9_res501.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile9_res501.log

resolution="--resolution 20 1"
out="--out profile9_res201.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile9_res201.log

resolution="--resolution 10 1"
out="--out profile9_res101.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile9_res101.log

resolution="--resolution 5 1"
out="--out profile9_res51.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile9_res51.log

resolution="--resolution 1 1"
out="--out profile9_res11.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile9_res11.log

# profile 10
file="data/blf/profile10"
resolution="--resolution 100 1"
out="--out profile10_res1001.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile10_res1001.log

resolution="--resolution 50 1"
out="--out profile10_res501.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile10_res501.log

resolution="--resolution 20 1"
out="--out profile10_res201.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile10_res201.log

resolution="--resolution 10 1"
out="--out profile10_res101.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile10_res101.log

resolution="--resolution 5 1"
out="--out profile10_res51.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile10_res51.log

resolution="--resolution 1 1"
out="--out profile10_res11.png"
config="$file $population $epochs $crossover_probability $elite $resolution $jobs $out"
echo $config
python blf_genetic/application.py $config > profile10_res11.log

