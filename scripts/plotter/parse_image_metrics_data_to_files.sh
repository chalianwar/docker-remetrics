
#!/bin/bash

awk -F',' '{print $2}' image_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst 
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > archival_size.txt 

awk -F',' '{print $1}' image_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > archival_to_gzip_ratio.txt

awk -F',' '{print $4}' image_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > file_cnt.txt

awk -F',' '{print $6}' image_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > dir_cnt.txt

awk -F',' '{print $7}' image_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > layer_cnt.txt

awk -F',' '{print $8}' image_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > compressed_size_with_method_gzip.txt

awk -F',' '{print $9}' image_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > uncompressed_sum_of_files.txt


awk -F',' '{print $10}' image_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > sum_to_gzip_ratio.txt


