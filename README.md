# clockwork-neutrino-lhco-pipeline

This repo contains code that was used in [https://arxiv.org/abs/1903.06191](https://arxiv.org/abs/1903.06191), for generating `.fr` files that can be used with Feynules, for feeding UFO model files and appropriate commands to `MadGraph_aMC@NLO` to simulate collider events, and analyse these collider events with kinematic variable cuts.

The FeynRules-MadGraph_aMC@NLO-Pythia-Delphes system of packages is used across the particle physics theory community for simulation and analysis of collider data, especially with Beyond Standard Model theories. The Clockwork neutrino model contains interacting sequences of sterile neutrinos which serve to explain the smallness of SM neutrinos. Creating model files and loading them to MadGraph is laborious in this case, because the neutrinos can number in the dozens. This repo contains scripts to make the process easy. The scripts use Python and bash, while FeynRules is a Mathematica package and requires Mathematica.

### FeynRules-Scripts

1. The script `GenFR.py` (and `GenFR_gen` for generalized clockwork neutrinos), given the clockwork parameters, calculate all the interaction couplings and generate the correct `.fr` file, which can then be used in FeynRules to make the model.
2. The `Clockwork_FeynRules_Script.wls` Wolfram Script then loads FeynRules and completes all the computations necessary to make the UFO directory that is used by MadGraph. It is assumed that you have Wolfram Scripts and FeynRules installed already. Edit the FeynRules and `.fr` model file path in the script before running. Note that the FeynRules calculation can take as long as 30 minutes or more. You will have to wait until the notebook finishes running.

### MadGraph-Scripts

1. The scripts `CW_*.sh` should be executed with bash to run MadGraph and simulate signal collider events. Paths to MadGraph, ROOT and the FeynRules models directory need to be updated before running the script. The hadron scripts are for proton-proton colliders and the lepton script is for an electron-positron collider. The suffix _lvl denotes generation of events that produce lepton-neutrino pairs instead of jets as in the un-suffixed case. The MadGraph commands in these scripts can be edited as needed, and should not be too challenging for a particle physicist with some experience with MadGraph. (Excellent tutorials are available online, such as [this one](https://www.physics.uci.edu/~tanedo/files/notes/ColliderMadgraph.pdf) by Prof. Flip Tanedo.)
2. `runMG_bkg_lvl.sh` is an example of a script for generating background events with MadGraph. This should be run *directly* with MadGraph's executable.

### Analysis-Mathematica

The Mathematica notebook in this folder contains many convenient functions for analysing `.lhco` files and plotting histograms of events. These are general and can be useful for analysis of other models as well! 


