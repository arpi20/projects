#!/bin/bash
g++ -w -O3 csearch.cpp porter.c -o searcher 
g++ -w -O3 merge.cpp -o merger

rm -rf 201101141_split_files
mkdir -p 201101141_split_files
cd 201101141_split_files
split -b 50M --suffix-length=4 ../$1
cd ..

python quantizing.py "201101141_split_files/"

rm -rf 201101141_indexes
mkdir -p 201101141_indexes


