
from algorithm_funcs import *

# image_metrics_datas = []

layer_metrics_datas = {}
image_mappers = []

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


def run_getmetrics_image_data():
    logging.info('=============> run_getmetricsdata <===========')

    load_image_mappers()

    calculate_repeat_layer_in_images()

    print "create pool"
    P1 = multiprocessing.Pool(60)
    print "before map"
    #image_metrics_datas = 
    P1.map(load_image_metrics_data, image_mappers)

    #for image_mapper in image_mappers:
    #    load_image_metrics_data(image_mapper)

    print "after map"

    #with open(os.path.join(dest_dir[0]['job_list_dir'], 'image_metrics_datas.json'), 'w+') as f_image_metrics_data:
    #   json.dump(image_metrics_datas, f_image_metrics_data)


def load_image_metrics_data(image_mapper):
    # image_mapper = {
    #     'version': version,
    #     'manifest': manifest_name_dir_map{},
    #     'config': config_name_dir_map{},
    #     'layers': layers_map{:{:}}
    # }

    processname = multiprocessing.current_process().name

    image_metrics_data = {}
    uncompressed_sum_of_files = 0
    compressed_size_with_method_gzip = 0
    archival_size = 0
    file_cnt = 0
    dir_cnt = 0
    layer_cnt = 0
    # image_name = None

    for key, val in image_mapper['layers'].items():
        for key1, val1 in val.items(): # only one entry
            layer_json_absfilename = val1 #json_absfilename
            if layer_json_absfilename is None:
                laogging.debug('The layer_json_absfilename is empty!')
                continue

            try:
                json_data = layer_metrics_datas[layer_json_absfilename]
            except:
                logging.debug("layer json file %s is not valid!", layer_json_absfilename)
                continue

            # if not os.path.isfile(layer_json_absfilename):
            #     logging.debug("layer json file %s is not valid!", layer_json_absfilename)
            #     continue

            logging.debug('process layer_json file: %s', layer_json_absfilename)  # str(layer_id).replace("/", "")

            # with open(layer_json_absfilename) as lj_f:
            #     try:
            #         json_data = json.load(lj_f)
            #     except:
            #         logging.debug("cannot load json file: layer json file %s is not valid!", layer_json_absfilename)
            #         lj_f.close()
            #         continue

            uncompressed_sum_of_files = uncompressed_sum_of_files + json_data['uncompressed_sum_of_files']
            compressed_size_with_method_gzip = compressed_size_with_method_gzip + json_data['compressed_size_with_method_gzip']
            archival_size = archival_size + json_data['archival_size']
	    layer_cnt = layer_cnt + 1
            file_cnt = file_cnt + json_data['file_cnt']
	    dir_cnt = dir_cnt + json_data['dir_cnt'] #len([x for x in json_data['dirs'] if x['subdir']])
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
    image_metrics_data['layer_cnt'] = layer_cnt
    image_metrics_data['file_cnt'] = file_cnt
    image_metrics_data['dir_cnt'] = dir_cnt
    image_metrics_data['version'] = image_mapper['version']
    image_metrics_data['image_name'] = image_mapper['manifest']

    logging.debug("image_metrics_data: %s", image_metrics_data)
    # return image_metrics_data
    with open('image_metrics_datas_%s.json' % processname, 'a+') as f_image_metrics_datas:
        json.dump(image_metrics_data, f_image_metrics_datas)
        f_image_metrics_datas.write(os.linesep)


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

    logging.debug(os.path.join(dest_dir[0]['job_list_dir'],'layer_metrics_datas_Poolworkers.json'))
    with open(os.path.join(dest_dir[0]['job_list_dir'],'layer_metrics_datas_Poolworkers.json'), 'r') as f:
        for line in f:
	    layer_data_json = {}
            data_json = json.loads(line)
            key = data_json['digest']
	    if not key:
		break
            print "read"+key
	
	    layer_data_json['archival_to_gzip_ratio'] = data_json['archival_to_gzip_ratio']
	    layer_data_json['dir_max_depth'] = data_json['dir_max_depth']
	    layer_data_json['archival_size'] = data_json['archival_size']
	    layer_data_json['file_cnt'] = data_json['file_cnt']
	    layer_data_json['dir_cnt'] = data_json['dir_cnt']

	    layer_data_json['compressed_size_with_method_gzip'] = data_json['compressed_size_with_method_gzip']
	    layer_data_json['uncompressed_sum_of_files'] = data_json['uncompressed_sum_of_files']
	    layer_data_json['sum_to_gzip_ratio'] = data_json['sum_to_gzip_ratio']

            layer_metrics_datas[key] = layer_data_json

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

    logging.debug("image_mapper[0]: %s", image_mappers[0])
