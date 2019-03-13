
#!/bin/bash

awk -F',' '{print $1}' file_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst 
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > stat_type.txt 

awk -F',' '{print $2}' file_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > sha256.txt

awk -F',' '{print $3}' file_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > type.txt

awk -F',' '{print $4}' file_metrics_datas_Poolworkers_without_null.json > tmp.txt
awk -F':' '{print $2}' tmp.txt > tmp.lst
tr < tmp.lst -d 'null' > file-without-nulls
grep -v -w '0' file-without-nulls > stat_size.txt

#awk -F',' '{print $7}' file_metrics_datas_Poolworkers_without_null.json > tmp.txt
#awk -F':' '{print $2}' tmp.txt > tmp.lst
#tr < tmp.lst -d 'null' > file-without-nulls
#grep -v -w '0' file-without-nulls > layer_cnt.txt
#
#awk -F',' '{print $8}' file_metrics_datas_Poolworkers_without_null.json > tmp.txt
#awk -F':' '{print $2}' tmp.txt > tmp.lst
#tr < tmp.lst -d 'null' > file-without-nulls
#grep -v -w '0' file-without-nulls > compressed_size_with_method_gzip.txt
#
#awk -F',' '{print $9}' file_metrics_datas_Poolworkers_without_null.json > tmp.txt
#awk -F':' '{print $2}' tmp.txt > tmp.lst
#tr < tmp.lst -d 'null' > file-without-nulls
#grep -v -w '0' file-without-nulls > uncompressed_sum_of_files.txt
#
#
#awk -F',' '{print $10}' file_metrics_datas_Poolworkers_without_null.json > tmp.txt
#awk -F':' '{print $2}' tmp.txt > tmp.lst
#tr < tmp.lst -d 'null' > file-without-nulls
#grep -v -w '0' file-without-nulls > sum_to_gzip_ratio.txt


