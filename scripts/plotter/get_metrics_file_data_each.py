
from algorithm_funcs import *

# image_mappers = []
# layer_mappers = []

# file_metrics_datas = []
# """file_metrics_data content
#     file size:
#     file type:
#     file extension:
#     sha256:
#     ctime
#     mtime
#     atime
#     uid
#     gid
# """


def run_getmetrics_file_data():
    logging.info('=============> run_getmetricsdata <===========')

    layer_mappers = load_layers_mappers()

    types = ['type', 'sha256', 'stat_type', 'stat_size']
    layer_mappers_slices = [layer_mappers[i:i + 24] for i in range(0, len(layer_mappers), 24)]

    for type in types:
        print "create pool"
        P2 = multiprocessing.Pool(60)
        print "before map"

        func = partial(load_file_metrics_data, type)

        P2.map(func, layer_mappers_slices)
	#for layer_mappers_slice in layer_mappers_slices:
	#    func(layer_mappers_slice)

        print "after map"


def load_file_metrics_data(type, _layer_mappers):

    processname = multiprocessing.current_process().name

    """file stat_type file type file size"""
    base_types = ['type', 'sha256']
    stat_types = ['stat_type', 'stat_size']

    file_metrics_data = []#defaultdict(list)

    for layer_mapper in _layer_mappers:
        for key, val in layer_mapper.items(): # only one entry
            #logging.debug("key: %s, val: %s!", key, val)
            layer_json_absfilename = val

            if not os.path.isfile(layer_json_absfilename):
                logging.debug("layer json file %s is not valid!", layer_json_absfilename)
                continue

            logging.debug('process layer_json file: %s, ===>%s', layer_json_absfilename, type)  # str(layer_id).replace("/", "")
            with open(layer_json_absfilename) as lj_f:
                try:
                    json_data = json.load(lj_f)
                except:
                    logging.debug("cannot load json file: layer json file %s is not valid!", layer_json_absfilename)
                    lj_f.close()
                    continue

                for subdir in json_data['dirs']:
                    for sub_file in subdir['files']:
                        if type in base_types:
                            file_metrics_data.append(sub_file[type])
                        elif type in stat_types:
                            file_metrics_data.append(sub_file['file_info'][type])

                del json_data

    logging.debug("file_metrics_data: number %s", len(file_metrics_data))
    with open('file_metrics_datas_%s-%s.json'%(type, processname), 'a+') as f_layer_metrics_datas:
        for data in file_metrics_data:
	    if data:
            	f_layer_metrics_datas.write(str(data) + '\n')

    # with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_metrics_datas_%s.json' % type),
    #           'w+') as f_layer_metrics_datas:
        # json.dump(file_metrics_datas, f_layer_metrics_datas)
    # return file_metrics_data


def load_layers_mappers():
    layer_mappers = []

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_mappers.json'), 'r') as f:
        _layer_mapper = json.load(f)

    for key, val in _layer_mapper.items():
        tmp_mapper = {}
        tmp_mapper[key] = val
        layer_mappers.append(tmp_mapper)

    return layer_mappers
