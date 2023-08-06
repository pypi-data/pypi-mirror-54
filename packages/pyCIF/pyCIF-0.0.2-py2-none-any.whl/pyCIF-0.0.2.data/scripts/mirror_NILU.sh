#!/usr/bin/env bash

# Fetching NILU version
cd 
mkdir NILU
cd NILU
git clone git@git.nilu.no:VERIFY/CIF.git ./
git fetch LSCE
git pull origin LSCE
git checkout LSCE

# Synchronizing with LSCE version
git remote set-url origin git@gitlab.in2p3.fr:satinv/cif.git
git pull origin LSCE

# Pushing to NILU
git remote set-url origin git@git.nilu.no:VERIFY/CIF.git
git push origin LSCE

rm -rf ~/NILU