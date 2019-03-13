
from algorithm_funcs import *

# layer_mappers = []

# image_metrics_datas = []
# """image_metrics_data content
#
#     version: schema1:
#             schema2:
#             schemalist:
#     size: compressed
#             sum of
#             archival
#     compression ratio:
#     repeat layer cnt:
#     file cnt:
#     layer depth:
# """

# layer_metrics_datas = []
"""layer_metrics_data content
    size: compressed
            sum of 
            archival
    compression ratio:
    repeat file cnt:
    file cnt:
    layer depth:
    file size:
    file type:
    
"""


def run_getmetrics_layer_data():
    logging.info('=============> run_getmetricsdata <===========')

    layer_mappers = load_layers_mappers()

    types = ['uncompressed_sum_of_files', 'compressed_size_with_method_gzip', 'archival_size', 'file_cnt', 'dir_cnt',
             'sum_to_gzip_ratio', 'archival_to_gzip_ratio', 'dir_max_depth', 'dir_min_depth', 'dir_median_depth', 'dir_avg_depth']
    layer_mappers_slices = [layer_mappers[i:i + 24] for i in range(0, len(layer_mappers), 24)]

    for type in types:
        print "create pool"
        P2 = multiprocessing.Pool(60)
        print "before map"

        func = partial(load_layer_metrics_data, type)

        layer_metrics_datas = P2.map(func, layer_mappers_slices)

        print "after map"

        #for layer_mapper in layer_mappers:
        #    load_layer_metrics_data(layer_mapper)

        with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_metrics_datas_%s.json'%type), 'w+') as f_layer_metrics_datas:
            json.dump(layer_metrics_datas, f_layer_metrics_datas)


def load_layer_metrics_data(type, _layer_mappers):

    types_size = ['uncompressed_sum_of_files', 'compressed_size_with_method_gzip', 'archival_size']
    types_depth = ['dir_max_depth', 'dir_min_depth', 'dir_median_depth', 'dir_avg_depth']
    types_ratio= ['sum_to_gzip_ratio', 'archival_to_gzip_ratio']

    _layer_metrics_data = []

    for layer_mapper in _layer_mappers:
        for key, val in layer_mapper.items(): # only one entry
            logging.debug("key: %s, val: %s!", key, val)
            layer_json_absfilename = val

            if not os.path.isfile(layer_json_absfilename):
                logging.debug("layer json file %s is not valid!", layer_json_absfilename)
                continue

            logging.debug('process layer_json file: %s', layer_json_absfilename)  # str(layer_id).replace("/", "")

            with open(layer_json_absfilename) as lj_f:
                try:
                    json_data = json.load(lj_f)
                except:
                    logging.debug("cannot load json file: layer json file %s is not valid!", layer_json_absfilename)
                    lj_f.close()
                    continue

                if type in types_size:
                    ret_data = json_data['size'][type]
                elif type in types_depth:
                    ret_data = json_data['layer_depth'][type]
                elif type == 'file_cnt':
                    ret_data = json_data['file_cnt']
                elif type == 'dir_cnt':
                    ret_data = len(json_data['dirs'])

                elif type in types_ratio:
                    compressed_size_with_method_gzip = json_data['size']['compressed_size_with_method_gzip']
                    if type == 'sum_to_gzip_ratio':
                        uncompressed_sum_of_files = json_data['size']['uncompressed_sum_of_files']
                        if compressed_size_with_method_gzip > 0:
                            ret_data = uncompressed_sum_of_files * 1.0 / compressed_size_with_method_gzip
                        else:
                            ret_data = None  # uncompressed_sum_of_files * 1.0 / compressed_size_with_method_gzip
                    elif type == 'archival_to_gzip_ratio':
                        archival_size = json_data['size']['archival_size']
                        if compressed_size_with_method_gzip > 0:
                            ret_data = archival_size * 1.0 / compressed_size_with_method_gzip
                        else:
                            ret_data = None  # archival_size * 1.0 / compressed_size_with_method_gzip

                del json_data

        logging.debug("layer_metrics_data: %s", ret_data)

        _layer_metrics_data.append(ret_data)
    return _layer_metrics_data


def load_layers_mappers():
    """load_image_mappers"""
    # image_mapper = {
    #     'version': version,
    #     'manifest': manifest_name_dir_map{},
    #     'config': config_name_dir_map{},
    #     'layers': layers_map{:{:}}
    # }

    layer_mappers = []

    with open(os.path.join(dest_dir[0]['job_list_dir'],'image_mapper.json'), 'r') as f:
        _image_mappers = json.load(f)

    logging.debug("load image_mapper: %s", os.path.join(dest_dir[0]['job_list_dir'],'image_mapper.json'))

    image_mappers = []

    for _image_mapper in _image_mappers:

        manifest_name_dir_map = {}
        config_name_dir_map = {}
        layers_map = {}

        for key, val in _image_mapper['manifest'].items():
            manifest_name_dir_map[key] = val

        if _image_mapper['config']:
            for key, val in _image_mapper['config'].items():
                config_name_dir_map[key] = val

        if _image_mapper['layers']:
            layer_name_dir_map = {}
            for key, val in _image_mapper['layers'].items():
                for key1, val1 in val.items():
                    layer_name_dir_map[key1] = val1
                layers_map[key] = layer_name_dir_map

        image_mapper = {
            'version': _image_mapper['version'],
            'manifest': manifest_name_dir_map,
            'config': config_name_dir_map,
            'layers': layers_map,
            'has_non_analyzed_layer_tarballs': _image_mapper['has_non_analyzed_layer_tarballs'],
            'has_non_downloaded_config': _image_mapper['has_non_downloaded_config']
        }

        image_mappers.append(image_mapper)
    
    logging.debug("image_mappers[0]: %s", image_mappers[0])

    layer_mapper = {}
    for image_mapper in image_mappers:
        for key, val in image_mapper['layers'].items():
            for key1, val1 in val.items(): # only one entry
                layer_json_absfilename = val1 #json_absfilename
                layer_mapper[key] = layer_json_absfilename


    for key, val in layer_mapper.items():
        tmp_mapper = {}
        tmp_mapper[key] = val
        layer_mappers.append(tmp_mapper)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_mappers.json'), 'w') as f:
        json.dump(layer_mapper, f)

    return layer_mappers
