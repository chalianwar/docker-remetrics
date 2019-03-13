
from algorithm_funcs import *
dest_dirname = "/home/nannan/2tb_hdd/"

def load_file_metrics_data_files():
    types = ['type', 'stat_type'] #'sha256'
    #defaultdict(list)
    print types
    for type in types:
        repeat_file_metrics_datas = {}
	print "load file"+os.path.join(dest_dirname, 'job_list_dir/file_metrics_datas_%s.json' % type)

        with open(os.path.join(dest_dirname, 'job_list_dir/file_metrics_datas_%s.json' % type),
                  'r') as f_layer_metrics_datas:
            for line in f_layer_metrics_datas:
                if type == 'type':
                    if line.split()[0] not in repeat_file_metrics_datas.keys():
                        repeat_file_metrics_datas[line.split()[0]] = 1
                    else:
                        repeat_file_metrics_datas[line.split()[0]] = repeat_file_metrics_datas[line.split()[0]] + 1
                else:
                    if line not in repeat_file_metrics_datas.keys():
                        repeat_file_metrics_datas[line] = 1
                    else:
                        repeat_file_metrics_datas[line] = repeat_file_metrics_datas[line] + 1
            # file_metrics_datas = json.load(f_layer_metrics_datas)
        calaculate_file_metrics(repeat_file_metrics_datas, type)
        del repeat_file_metrics_datas

    file_metrics_datas = []
    with open(os.path.join(dest_dirname, 'job_list_dir/file_metrics_datas_%s.json' % 'sha256'),
                  'r') as f_layer_metrics_datas:
        for line in f_layer_metrics_datas:
            file_metrics_datas.append(line)

        calaculate_file_metrics(file_metrics_datas, 'sha256')

def calaculate_file_metrics(file_metrics_datas, type):
    """get repeat files"""
    if type == 'sha256':
        file_dict = calculate_repeates(file_metrics_datas)
    else:
        file_dict = file_metrics_datas
    print "write to"+os.path.join(dest_dirname, 'job_list_dir/repeate_file_%s.json'%type)
    with open(os.path.join(dest_dirname, 'job_list_dir/repeate_file_%s.json'%type), 'w') as f:
        json.dump(file_dict, f)


def main():
    load_file_metrics_data_files()


if __name__ == '__main__':
    print 'start!'
    main()
    print 'finished!'
