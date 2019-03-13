
#!/bin/bash

awk -F',' '{print $4}' layer_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst 
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > archival_size.txt 

awk -F',' '{print $3}' layer_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > archival_to_gzip_ratio.txt

awk -F',' '{print $5}' layer_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > file_cnt.txt

awk -F',' '{print $7}' layer_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > dir_cnt.txt

awk -F',' '{print $1}' layer_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > dir_max_depth.txt

awk -F',' '{print $8}' layer_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > compressed_size_with_method_gzip.txt

awk -F',' '{print $9}' layer_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > uncompressed_sum_of_files.txt


awk -F',' '{print $12}' layer_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > sum_to_gzip_ratio.txt


