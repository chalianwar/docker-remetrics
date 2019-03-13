
from draw_pic import *

image_mappers = []
layer_mappers = []

image_metrics_datas = []
"""image_metrics_data content

    version: schema1:
            schema2:
            schemalist:
    size: compressed
            sum of 
            archival
    compression ratio:
    repeat layer cnt:
    file cnt:
    layer depth:
"""

layer_metrics_datas = []
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

file_metrics_datas = []
"""file_metrics_data content
    file size:
    file type:
    file extension:
    sha256:
    ctime
    mtime
    atime
    uid
    gid
"""


def run_getmetricsdata():
    logging.info('=============> run_getmetricsdata <===========')

    load_image_mappers()
    load_layers_mappers()

    #calculate_repeat_layer_in_images()

    print "create pool"
    #P1 = multiprocessing.Pool(60)
    print "before map"
    #image_metrics_datas = P1.map(load_image_metrics_data, image_mappers)

    #for image_mapper in image_mappers:
    #    load_image_metrics_data(image_mapper)

    print "after map"

    #with open("image_metrics_datas.json", 'w+') as f_image_metrics_data:
    #    json.dump(image_metrics_datas, f_image_metrics_data)

    print "create pool"
    P2 = multiprocessing.Pool(10)
    print "before map"

    layer_mappers_slices = [layer_mappers[i:i + 24] for i in range(0, len(layer_mappers), 24)]
    layer_metrics_datas = P2.map(load_layer_metrics_data, layer_mappers_slices)

    print "after map"

    #for layer_mapper in layer_mappers:
    #    load_layer_metrics_data(layer_mapper)

    with open("layer_metrics_datas.json", 'w+') as f_layer_metrics_datas:
        json.dump(layer_metrics_datas, f_layer_metrics_datas)

    calaculate_file_metrics()

def load_layer_metrics_data(_layer_mappers):
    uncompressed_sum_of_files = 0
    compressed_size_with_method_gzip = 0
    archival_size = 0
    file_cnt = 0

    dir_max_depth = 0
    dir_min_depth = 0
    dir_median_depth = 0
    dir_avg_depth = 0

    dir_cnt = 0

    _layer_metrics_data = []

    for layer_mapper in _layer_mappers:
        layer_dir_files = []
        layer_metrics_data = {}
        for key, val in layer_mapper.items(): # only one entry
            logging.debug("key: %s, val: %s!", key, val)
            layer_json_absfilename = val

            if not os.path.isfile(layer_json_absfilename):
                logging.debug("layer json file %s is not valid!", layer_json_absfilename)
                continue

            logging.debug('process layer_json file: %s', layer_json_absfilename)  # str(layer_id).replace("/", "")
            # json_data = None
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
                dir_cnt = len(json_data['dirs'])

                for subdir in json_data['dirs']:
            #dir_cnt = dir_cnt + 1
                    for sub_file in subdir['files']:
                        layer_dir_files.append(sub_file)

                del json_data
            # lj_f.close()

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

        layer_metrics_data['files'] = layer_dir_files

        logging.debug("layer_metrics_data['sum_to_gzip_ratio']: %s", layer_metrics_data['sum_to_gzip_ratio'])
        # gc.collect()
        _layer_metrics_data.append(layer_metrics_data)
    return _layer_metrics_data


def load_image_metrics_data(image_mapper):
    # image_mapper = {
    #     'version': version,
    #     'manifest': manifest_name_dir_map{},
    #     'config': config_name_dir_map{},
    #     'layers': layers_map{:{:}}
    # }
    image_metrics_data = {}
    uncompressed_sum_of_files = 0
    compressed_size_with_method_gzip = 0
    archival_size = 0
    file_cnt = 0

    for key, val in image_mapper['layers'].items():
        for key1, val1 in val.items(): # only one entry
            layer_json_absfilename = val1 #json_absfilename
            if layer_json_absfilename is None:
                laogging.debug('The layer_json_absfilename is empty!')
                continue

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

                uncompressed_sum_of_files = uncompressed_sum_of_files + json_data['size']['uncompressed_sum_of_files']
                compressed_size_with_method_gzip = compressed_size_with_method_gzip + json_data['size']['compressed_size_with_method_gzip']
                archival_size = archival_size + json_data['size']['archival_size']

                file_cnt = file_cnt + json_data['file_cnt']

                del json_data

    image_metrics_data['uncompressed_sum_of_files'] = uncompressed_sum_of_files
    image_metrics_data['compressed_size_with_method_gzip'] = compressed_size_with_method_gzip
    image_metrics_data['archival_size'] = archival_size

    if compressed_size_with_method_gzip > 0:
        image_metrics_data['sum_to_gzip_ratio'] = uncompressed_sum_of_files * 1.0 / compressed_size_with_method_gzip
        image_metrics_data['archival_to_gzip_ratio'] = archival_size * 1.0 / compressed_size_with_method_gzip
    else:
        image_metrics_data['sum_to_gzip_ratio'] = None #uncompressed_sum_of_files * 1.0 / compressed_size_with_method_gzip
        image_metrics_data['archival_to_gzip_ratio'] = None #archival_size * 1.0 / compressed_size_with_method_gzip

    image_metrics_data['file_cnt'] = file_cnt

    image_metrics_data['version'] = image_mapper['version']

    logging.debug("image_metrics_data: %s", image_metrics_data)
    return image_metrics_data


def calculate_repeates(l):
    logging.info("first file_sha256s list: %s", l[0])
    #l_dict = {i: l.count(i) for i in l}
    l_dict = pd.DataFrame(l, columns=["x"]).groupby('x').size().to_dict()
    #for key, val in l.items():
    #    logging.debug(key, val)

    return l_dict


def calaculate_file_metrics():
    """get repeat files"""
    _file_metrics_datas = []

    _layer_metrics_datas = list(chain(*layer_metrics_datas))

    for layer_metrics_data in _layer_metrics_datas:
        layer_dir_files = layer_metrics_data['files']
        _file_metrics_datas.append(layer_dir_files)

    file_metrics_datas = list(chain(*_file_metrics_datas))
    
    with open(os.path.join(dest_dir[0]['job_list_dir'], 'file_metrics_datas.json'), 'w') as f:
        json.dump(file_metrics_datas, f)

    file_sha256s = []
    file_types = []
    file_stat_types = []
    file_stat_sizes = []

    for dir_file in file_metrics_datas:
        file_sha256s.append(dir_file['sha256'])

    file_sha256s_dict = calculate_repeates(file_sha256s)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'repeate_file_sha256s.json'), 'w') as f:
        json.dump(file_sha256s_dict, f)

    """file types"""

    for dir_file in file_metrics_datas:
        file_types.append(dir_file['type'])

    file_types_dict = calculate_repeates(file_types)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'repeate_file_types_dict.json'), 'w') as f:
        json.dump(file_types_dict, f)

    """file stat_type"""

    for dir_file in file_metrics_datas:
        file_stat_types.append(dir_file['file_info']['stat_type'])

    file_types_dict = calculate_repeates(file_stat_types)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'repeate_file_types_dict.json'), 'w') as f:
        json.dump(file_types_dict, f)

    """file size"""

    for dir_file in file_metrics_datas:
        file_stat_sizes.append(dir_file['file_info']['stat_size'])

    file_stat_sizes_dict = calculate_repeates(file_stat_sizes)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'repeate_file_stat_sizes_dict.json'), 'w') as f:
        json.dump(file_stat_sizes_dict, f)


def calculate_repeat_layer_in_images():
    layer_digests = []

    for image_mapper in image_mappers:
        image_layer_digests = []
        for key, val in image_mapper['layers'].items():
            image_layer_digests.append(key)
        layer_digests.append(image_layer_digests)

    logging.info("first layer_digests list: %s", layer_digests[0])

    layer_digests_union = list(chain(*layer_digests))

    logging.info("first layer_digests list: %s", layer_digests_union[0])

    """note that we remove the duplicates from schema 1's layer digests in contruct_image_mapper.py"""

    layer_digests_dict = calculate_repeates(layer_digests_union)

    #layer_digests_dict = {i: layer_digests_union.count(i) for i in layer_digests_union}
    #for key, val in layer_digests_dict.items():
    #    logging.debug(key, val)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'repeate_layer_digests_dict.json'), 'w') as f:
        json.dump(layer_digests_dict, f)


def load_image_mappers():
    """load_image_mappers"""
    # image_mapper = {
    #     'version': version,
    #     'manifest': manifest_name_dir_map{},
    #     'config': config_name_dir_map{},
    #     'layers': layers_map{:{:}}
    # }

    with open(os.path.join(dest_dir[0]['job_list_dir'],'image_mapper.json'), 'r') as f:
        _image_mappers = json.load(f)

    logging.debug("load image_mapper: %s", os.path.join(dest_dir[0]['job_list_dir'],'image_mapper.json'))

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


def load_layers_mappers():
    layer_mapper = {}
    for image_mapper in image_mappers:
        for key, val in image_mapper['layers'].items():
            for key1, val1 in val.items(): # only one entry
                layer_json_absfilename = val1 #json_absfilename
                layer_mapper[key] = layer_json_absfilename

    #print layer_mapper    

    for key, val in layer_mapper.items():
        tmp_mapper = {}
        tmp_mapper[key] = val
        layer_mappers.append(tmp_mapper)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_mappers.json'), 'w') as f:
        json.dump(layer_mapper, f)

#    for key, val in layer_mapper:
#        tmp_mapper = {}
#        tmp_mapper[key] = val
#        layer_mappers.append(tmp_mapper)


