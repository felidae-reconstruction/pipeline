cut -f2,3 $1 > tmp_start_end.lst
cat tmp_start_end.lst | awk '$a=$2 - $1 {print $a}' > tmp_lengths.lst 
awk '{ sum += $1 } END { print sum }' tmp_lengths.lst
rm tmp_start_end.lst
rm tmp_lengths.lst
