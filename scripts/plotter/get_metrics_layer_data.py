
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
    # layer_metrics_datas = []

    # load_layers_mappers()

    print "create pool"
    P2 = multiprocessing.Pool(60)
    print "before map"

    layer_mappers_slices = [layer_mappers[i:i + 24] for i in range(0, len(layer_mappers), 24)]
    P2.map(load_layer_metrics_data, layer_mappers_slices)

    print "after map"

    #for layer_mapper in layer_mappers:
    #    load_layer_metrics_data(layer_mapper)

    # with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_metrics_datas.json'), 'w+') as f_layer_metrics_datas:
    #     json.dump(layer_metrics_datas, f_layer_metrics_datas)


def load_layer_metrics_data(_layer_mappers):

    processname = multiprocessing.current_process().name

    uncompressed_sum_of_files = 0
    compressed_size_with_method_gzip = 0
    archival_size = 0
    file_cnt = 0

    dir_max_depth = 0
    dir_min_depth = 0
    dir_median_depth = 0
    dir_avg_depth = 0

    dir_cnt = 0

    # _layer_metrics_data = []

    # base_types = ['type', 'sha256']
    # stat_types = ['stat_type', 'stat_size']

    digest = None

    file_metrics_data = {}

    for layer_mapper in _layer_mappers:
        layer_metrics_data = {}
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

                uncompressed_sum_of_files = json_data['size']['uncompressed_sum_of_files']
                compressed_size_with_method_gzip = json_data['size']['compressed_size_with_method_gzip']
                archival_size = json_data['size']['archival_size']

                dir_max_depth = json_data['layer_depth']['dir_max_depth']
                dir_min_depth = json_data['layer_depth']['dir_min_depth']
                dir_median_depth = json_data['layer_depth']['dir_median_depth']
                dir_avg_depth = json_data['layer_depth']['dir_avg_depth']

                file_cnt = json_data['file_cnt']
                dir_cnt = len([x for x in json_data['dirs'] if x['subdir']])
                digest = layer_json_absfilename

                for subdir in json_data['dirs']:
                    for sub_file in subdir['files']:
                        file_metrics_data['type'] = sub_file['type']
                        file_metrics_data['sha256'] = sub_file['sha256']

                        file_metrics_data['stat_type'] = sub_file['file_info']['stat_type'] #['sha256']
                        file_metrics_data['stat_size'] = sub_file['file_info']['stat_size']

                        with open('file_metrics_datas_%s.json' % processname, 'a+') as f_file_metrics_datas:
                            json.dump(file_metrics_data, f_file_metrics_datas)
                            f_file_metrics_datas.write(os.linesep)

                        # if type in base_types:
                        #     file_metrics_data.append(sub_file[type])
                        # elif type in stat_types:
                        #     file_metrics_data.append(sub_file['file_info'][type])

                del json_data

        layer_metrics_data['uncompressed_sum_of_files'] = uncompressed_sum_of_files
        layer_metrics_data['compressed_size_with_method_gzip'] = compressed_size_with_method_gzip
        layer_metrics_data['archival_size'] = archival_size
        if compressed_size_with_method_gzip > 0:
            layer_metrics_data['sum_to_gzip_ratio'] = uncompressed_sum_of_files * 1.0 / compressed_size_with_method_gzip
            layer_metrics_data['archival_to_gzip_ratio'] = archival_size * 1.0 / compressed_size_with_method_gzip
        else:
            layer_metrics_data['sum_to_gzip_ratio'] = None #uncompressed_sum_of_files * 1.0 / compressed_size_with_method_gzip
            layer_metrics_data['archival_to_gzip_ratio'] = None#archival_size * 1.0 / compressed_size_with_method_gzip


        layer_metrics_data['dir_max_depth'] = dir_max_depth
        layer_metrics_data['dir_min_depth'] = dir_min_depth
        layer_metrics_data['dir_median_depth'] = dir_median_depth
        layer_metrics_data['dir_avg_depth'] = dir_avg_depth

        layer_metrics_data['file_cnt'] = file_cnt
        layer_metrics_data['dir_cnt'] = dir_cnt

        layer_metrics_data['digest'] = digest

        logging.debug("layer_metrics_data: %s", layer_metrics_data)

        # logging.debug("layer_metrics_data: number %s", len(file_metrics_data))
        # with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_metrics_datas-%s.json' % processname),
        #           'a+') as f_layer_metrics_datas:
        #     for data in file_metrics_data:
        #         f_layer_metrics_datas.write(data + '\n')
        with open('layer_metrics_datas_%s.json' % processname, 'a+') as f_layer_metrics_datas:
            json.dump(layer_metrics_data, f_layer_metrics_datas)
            f_layer_metrics_datas.write(os.linesep)


            # for data in file_metrics_data:
            #     if data:
            #         f_layer_metrics_datas.write(str(data) + '\n')
        # _layer_metrics_data.append(layer_metrics_data)
    # return _layer_metrics_data


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


# def load_layers_mappers():
#     layer_mapper = {}
#     for image_mapper in image_mappers:
#         for key, val in image_mapper['layers'].items():
#             for key1, val1 in val.items(): # only one entry
#                 layer_json_absfilename = val1 #json_absfilename
#                 layer_mapper[key] = layer_json_absfilename
#
#
#     for key, val in layer_mapper.items():
#         tmp_mapper = {}
#         tmp_mapper[key] = val
#         layer_mappers.append(tmp_mapper)
#
#     with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_mappers.json'), 'w') as f:
#         json.dump(layer_mapper, f)



