#!/bin/bash

# Clockwork parameters
N=$1
m1=$2

# Hadron collider energy in TeV
E=$3
Ehalf=$(($E/2))

# Choose working directory. Also add path to FeynRules models, and correct name for UFO directory
cd ~/Clockwork/
mv ~/path/to/FeynRules/models/Clockwork_UFO /path/to/MadGraph/models/Clockwork_Neutrino_UFO

# Creates script to run MadGraph with ALL CW neutrinos
rm runMG*.sh
>runMG_$N.sh
echo "import model Clockwork_Neutrino_UFO">>runMG_$N.sh
str="define n = ns11 ns11~ ns12 ns12~ ns13 ns13~"    

for i in `seq 2 $N`;
do
    str=$str" ns"$i"1 ns"$i"1~ ns"$i"2 ns"$i"2~ ns"$i"3 ns"$i"3~"
done

echo $str>>runMG_$N.sh

# Add processes you want to run, kinematic cuts etc.
echo "generate p p > e- e+ w+ / a z h vl vl~, w+ > l+ vl QCD=99 QED=99">>runMG_$N.sh
echo "add process p p > e- e+ w- / a z h vl vl~, w- > l- vl~ QCD=99 QED=99">>runMG_$N.sh
echo "add process p p > mu- mu+ w+ / a z h vl vl~, w+ > l+ vl QCD=99 QED=99">>runMG_$N.sh
echo "add process p p > mu- mu+ w- / a z h vl vl~, w- > l- vl~ QCD=99 QED=99">>runMG_$N.sh
echo "output clockwork_lvl_"$N"_"$m1"_GeV_"$E"_TeV">>runMG_$N.sh
echo "launch">>runMG_$N.sh
echo "shower=PYTHIA8">>runMG_$N.sh
echo "delphes=ON">>runMG_$N.sh

for i in `seq 1 $N`;
do
    num=$(expr 990000 + $i)
    echo "set width "$num"1 Auto">>runMG_$N.sh
    echo "set width "$num"2 Auto">>runMG_$N.sh
    echo "set width "$num"3 Auto">>runMG_$N.sh
done

echo "set nevents 100000">>runMG_$N.sh
echo "set ebeam1 "$Ehalf"000.0">>runMG_$N.sh
echo "set ebeam2 "$Ehalf"000.0">>runMG_$N.sh
echo "set cut_decays True">>runMG_$N.sh
echo "set ptj 50.0">>runMG_$N.sh
echo "set ptl 50.0">>runMG_$N.sh


# Load ROOT from appropriate directory (required for MadGraph)
source ~/root-6.06.06.sl7/bin/thisroot.sh

# Add path to MadGraph executable
/path/to/MadGraph/MG5_aMC_v2_6_4/bin/mg5_aMC runMG_$N.sh
