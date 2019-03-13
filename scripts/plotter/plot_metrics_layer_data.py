

from draw_pic import *

uncompressed_sum_of_files = []
compressed_size_with_method_gzip = []
archival_size = []
sum_to_gzip_ratio = []
archival_to_gzip_ratio = []
file_cnt = []

dir_max_depth = []
dir_min_depth = []
dir_median_depth = []
dir_avg_depth = []

dir_cnt = []


def run_plotmetrics_layer_data():
    load_layer_metrics_data_file()
    try:
        plot_graph('uncompressed_sum_of_files')
    except:
        print "Cannot plot uncompressed_sum_of_files", sys.exc_info()
        traceback.print_exc(file=sys.stdout)
    try:
        plot_graph('compressed_size_with_method_gzip')
    except:
        print "cannot plot compressed_size_with_method_gzip", sys.exc_info()
        traceback.print_exc(file=sys.stdout)
    try:
        plot_graph('archival_size')
    except:
        print "cannot print archival_size", sys.exc_info()
        traceback.print_exc(file=sys.stdout)

    try:
        plot_graph('sum_to_gzip_ratio')
    except:
        print "cannot print sum_to_gzip_ratio", sys.exc_info()
        traceback.print_exc(file=sys.stdout)
    try:
        plot_graph('archival_to_gzip_ratio')
    except:
        print "cannot print archival_to_gzip_ratio", sys.exc_info()
        traceback.print_exc(file=sys.stdout)

    try:
        plot_graph('file_cnt')
    except:
        print "cannot print file_cnt", sys.exc_info()
        traceback.print_exc(file=sys.stdout)
    try:
        plot_graph('dir_cnt')
    except:
        print "cannot print dir_cnt", sys.exc_info()
        traceback.print_exc(file=sys.stdout)

    try:
        plot_graph('dir_max_depth')
    except:
        print "cannot print dir_max_depth", sys.exc_info()
        traceback.print_exc(file=sys.stdout)


def plot_graph(type):

    print "===========> plot %s <=========="%type
    fig = fig_size('min')#min')  # 'large'
    #fig = fig_size('large')
    y_type = "layers"
    if type == 'uncompressed_sum_of_files':
        data1 = uncompressed_sum_of_files
        xlabel = 'Uncompressed layer size (MB) as sum of files'
        data = [x * 1.0 / 1024 / 1024 for x in data1]
        xlim = int(mean(data))
	#xlim = max(data)
    elif type == 'compressed_size_with_method_gzip':
        data1 = compressed_size_with_method_gzip
        xlabel = 'Compressed layer tarball size (MB)'
        data = [x * 1.0 / 1024 / 1024 for x in data1]
        xlim = 50
	#xlim = max(data)
    elif type == 'archival_size':
        data1 = archival_size
        xlabel = 'Uncompressed layer tarball size (MB)'
        data = [x * 1.0 / 1024 / 1024 for x in data1]
        xlim = 250
	#xlim = max(data)
    elif type == 'sum_to_gzip_ratio':
        data = sum_to_gzip_ratio
        xlabel = 'Compression ratio: Uncompressed layer size as sum of files / compressed_size_with_method_gzip'
        xlim = 10
	#xlim = max(data)
    elif type == 'archival_to_gzip_ratio':
        data = archival_to_gzip_ratio
        xlabel = 'Compression ratio: Uncompressed layer tarball size / compressed_size_with_method_gzip'
        xlim = 100
	#xlim = max(data)
    elif type == 'file_cnt':
        data = file_cnt
        xlabel = 'File count for each image'
        xlim = 50
	#xlim = max(data)
    elif type == 'dir_cnt':
        data = dir_cnt
        xlabel = 'Layer directory count across all images'
        xlim = 200
	#xlim = max(data)
    elif type == 'dir_max_depth':
        data = dir_max_depth
        xlabel = 'Layer directory depth for each image'
        xlim = 25
	#xlim = max(data)

    print "xlim = %f, len = %d"%(xlim, len(data))
    plot_cdf(fig, data, xlabel, xlim, 0, y_type)

""""        archival_size": 58003968,
            "archival_to_gzip_ratio": 3.194986725738297,
            "compressed_size_with_method_gzip": 18154682,
            "dir_avg_depth": 4.337016574585635,
            "dir_cnt": 543,
            "dir_max_depth": 9,
            "dir_median_depth": 4,
            "dir_min_depth": 1,
            "file_cnt": 4271,
            "sum_to_gzip_ratio": 3.0582276241467627,
            "uncompressed_sum_of_files": 55521150
"""

def load_layer_metrics_data_file():

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_metrics_datas.json'), 'r') as f_layer_metrics_datas:
        _json_datas = json.load(f_layer_metrics_datas)

        json_datas = list(chain(*_json_datas))

        print json_datas[0]

        for json_data in json_datas:
            uncompressed_sum_of_files.append(json_data['uncompressed_sum_of_files'])
            compressed_size_with_method_gzip.append(json_data['compressed_size_with_method_gzip'])
            archival_size.append(json_data['archival_size'])

            sum_to_gzip_ratio.append(json_data['sum_to_gzip_ratio'])
            archival_to_gzip_ratio.append(json_data['archival_to_gzip_ratio'])
            file_cnt.append(json_data['file_cnt'])

            dir_max_depth.append(json_data['dir_max_depth'])
            # dir_min_depth = []
            # dir_median_depth = []
            # dir_avg_depth = []

            dir_cnt.append(json_data['dir_cnt'])

