#!/usr/bin/env bash

cd ~/CIF
git remote set-url origin https://berchet@git.nilu.no/VERIFY/CIF.git
git push origin master:LSCE



git remote set-url origin https://antoine.berchet@gitlab.in2p3.fr/satinv/cif.git


mkdir NILU
git clone git@gitlab.in2p3.fr:satinv/cif.git
git remote set-url origin git@git.nilu.no:VERIFY/CIF.git
git fetch origin LSCE
git checkout LSCE
git merge master
git push origin LSCE



