#!/bin/bash
for file in `ls 201101141_split_files`
do
  ./searcher "201101141_split_files/$file" 
done

./merger "./201101141_indexes/"  $1
   
