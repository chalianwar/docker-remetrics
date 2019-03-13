

from draw_pic import *

def run_parsemetrics_data():
    load_file_metrics_data_file()
    load_layer_metrics_data_file()
    load_image_metrics_data_file()


def load_image_metrics_data_file():
    print "load file" + os.path.join(dest_dir[0]['job_list_dir'], 'image_metrics_datas_Poolworkers.json')
    with open(os.path.join(dest_dir[0]['job_list_dir'], 'image_metrics_datas_Poolworkers.json'), 'r') as f_image_metrics_data:
        for line in f_image_metrics_data:
            json_data = json.load(line)

            uncompressed_sum_of_files = json_data['uncompressed_sum_of_files']
            write_to_file('uncompressed_sum_of_files', uncompressed_sum_of_files, 'image')
            compressed_size_with_method_gzip = json_data['compressed_size_with_method_gzip']
            write_to_file('compressed_size_with_method_gzip', compressed_size_with_method_gzip, 'image')
            archival_size = json_data['archival_size']
            write_to_file('archival_size', archival_size, 'image')

            sum_to_gzip_ratio = json_data['sum_to_gzip_ratio']
            write_to_file('sum_to_gzip_ratio', sum_to_gzip_ratio, 'image')
            archival_to_gzip_ratio = json_data['archival_to_gzip_ratio']
            write_to_file('archival_to_gzip_ratio', archival_to_gzip_ratio, 'image')
            file_cnt = json_data['file_cnt']
            write_to_file('file_cnt', file_cnt, 'image')
            dir_cnt = json_data['dir_cnt']
            write_to_file('dir_cnt', dir_cnt, 'image')
            layer_cnt = json_data['layer_cnt']
            write_to_file('layer_cnt', layer_cnt, 'image')

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'repeate_layer_digests_dict.json'), 'r') as f_repeate_layer_digests_dict:
        json_datas = json.load(f_repeate_layer_digests_dict)
        for key, val in json_datas.items():
            write_to_file('repeate_layer_digests', val, 'image')


def load_layer_metrics_data_file():
    print "load file" + os.path.join(dest_dir[0]['job_list_dir'], 'layer_metrics_datas_Poolworkers.json')
    with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_metrics_datas_Poolworkers.json'), 'r') as f_layer_metrics_datas:
        for line in f_layer_metrics_datas:
            json_data = json.load(line)

            uncompressed_sum_of_files = json_data['uncompressed_sum_of_files']
            write_to_file('uncompressed_sum_of_files', uncompressed_sum_of_files, 'layer')
            compressed_size_with_method_gzip = json_data['compressed_size_with_method_gzip']
            write_to_file('compressed_size_with_method_gzip', compressed_size_with_method_gzip, 'layer')
            archival_size = json_data['archival_size']
            write_to_file('archival_size', archival_size, 'layer')

            sum_to_gzip_ratio = json_data['sum_to_gzip_ratio']
            write_to_file('sum_to_gzip_ratio', sum_to_gzip_ratio, 'layer')
            archival_to_gzip_ratio = json_data['archival_to_gzip_ratio']
            write_to_file('archival_to_gzip_ratio', archival_to_gzip_ratio, 'layer')
            file_cnt = json_data['file_cnt']
            write_to_file('file_cnt', file_cnt, 'layer')

            dir_max_depth = json_data['dir_max_depth']
            write_to_file('dir_max_depth', dir_max_depth, 'layer')
            # dir_min_depth = []
            # dir_median_depth = []
            # dir_avg_depth = []

            dir_cnt = json_data['dir_cnt']
            write_to_file('dir_cnt', dir_cnt, 'layer')


def load_file_metrics_data_file():
    print "load file"+os.path.join(dest_dir[0]['job_list_dir'], 'file_metrics_datas_Poolworkers.json')
    with open(os.path.join(dest_dir[0]['job_list_dir'], 'file_metrics_datas_Poolworkers.json'), 'r') as f_file_metrics_data:
        for line in f_file_metrics_data:
            json_data = json.load(line)

            stat_size = json_data['stat_size']
            write_to_file('stat_size', stat_size, 'file')
            stat_type = json_data['stat_type']
            write_to_file('stat_type', stat_type, 'file')
            type = json_data['type']
            write_to_file('type', type, 'file')
            sha256 = json_data['sha256']
            write_to_file('sha256', sha256, 'file')

