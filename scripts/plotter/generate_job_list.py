from draw_pic import *

def run_generatejoblist():
    logging.info('=============> run_generatejoblist <===========')

    bad_image_mappers = load_bad_image_mappers()
    image_mappers = load_image_mappers()
    analyzed_layers = load_layers_mappers()

    print "analyzed_layers: %d" % analyzed_layers

    list_50mb = load_job_list('list_less_50m.out')
    list_1gb = load_job_list('list_less_1g.out')
    list_2gb = load_job_list('list_less_2g.out')
    list_b_2gb = load_job_list('list_bigger_2g.out')

    config = []
    _digests = []
    image_names_with_no_configs = 0
    image_names_with_no_analyzed_layers = 0

    image_names_with_full_analyzed_layers = 0    
    image_names = 0

    layer_list_50mb = {}
    layer_list_1gb = {}
    layer_list_2gb = {}
    layer_list_b_2gb = {}

    bad_layer_downloader_job_list = defaultdict(list)

    unique_digest = {}

    for image_mapper in bad_image_mappers:
	#print image_mapper['bad_manifest']
	if image_mapper['non_downloaded_config_digest']:
            config.append(image_mapper['non_downloaded_config_digest'])
	if len(image_mapper['non_analyzed_layer_tarballs_digests']):
            _digests.append(image_mapper['non_analyzed_layer_tarballs_digests'])
            for digest in image_mapper['non_analyzed_layer_tarballs_digests']:
		try:
		    a = unique_digest[digest]
		except:
		    #if digest not in unique_digest:
                    unique_digest[digest] = True
                    bad_layer_downloader_job_list[image_mapper['bad_manifest']].append(digest) #= image_mapper['non_analyzed_layer_tarballs_digests']

    digests = list(set(list(chain(*_digests))))
    print len(digests)
    print "check the size"

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'bad_layer_downloader_job_list.out'), 'w+') as f_out:
        json.dump(bad_layer_downloader_job_list, f_out)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'non_analyzed_layer_digests.out'), 'w+') as f_out:
        #json.dump(layer_list_50mb, f_out)
	for digest in digests:
	    f_out.write(digest+'\n')

    for image_mapper in image_mappers:
	image_names = image_names + 1
        if image_mapper['has_non_downloaded_config']:
            image_names_with_no_configs = image_names_with_no_configs + 1
        if image_mapper['has_non_analyzed_layer_tarballs']:
            image_names_with_no_analyzed_layers = image_names_with_no_analyzed_layers + 1
	if not image_mapper['has_non_analyzed_layer_tarballs']:
	    image_names_with_full_analyzed_layers = image_names_with_full_analyzed_layers + 1

    print "image_names_with_no_configs: %d" % image_names_with_no_configs
    print "image_names_with_no_analyzed_layers: %d" % image_names_with_no_analyzed_layers
    print "image_names_with_full_analyzed_layers: %d" % image_names_with_full_analyzed_layers
    print "image_names: %d" % image_names

    """check the size"""
    for digest in digests:
        try:
            val = list_50mb[digest]
        except:
            pass
        else:
            layer_list_50mb.update(val)

        try:
            val = list_1gb[digest]
        except:
            pass
        else:
            layer_list_1gb.update(val)

        try:
            val = list_2gb[digest]
        except:
            pass
        else:
            layer_list_2gb.update(val)

        try:
            val = list_b_2gb[digest]
        except:
            pass
        else:
            layer_list_b_2gb.update(val)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_list_less_50m.out'), 'w+') as f_out:
        json.dump(layer_list_50mb, f_out)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_list_less_1g.out'), 'w+') as f_out:
        json.dump(layer_list_1gb, f_out)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_list_less_2g.out'), 'w+') as f_out:
        json.dump(layer_list_2gb, f_out)

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_list_bigger_2g.out'), 'w+') as f_out:
        json.dump(layer_list_b_2gb, f_out)


def extract_layer_config_name(filename):
    sstr = filename.split("-")
    if len(sstr) > 1:
    	name = "sha256:"+sstr[1]
    #print "layer or config: name: %s, abs_filename: %s"%(name, filename)
    	return name
    else:
        print "layer or config: filename: %s" % filename
	return None


def load_job_list(filename):
    job_dict = {}
    with open(os.path.join(dest_dir[0]['job_list_dir'], filename), 'r') as f:
        json_data = json.load(f)

    for key, val in json_data.items():
        tmp_dict = {}
        tmp_dict[key] = val
        digest = extract_layer_config_name(key)
	if digest:
            job_dict[digest] = tmp_dict

    print "load job list"
    return job_dict


def load_bad_image_mappers():
    """load_image_mappers"""
    # bad_image_mapper = {
    #     'version': version,
    #     'bad_manifest': manifest_name_dir_map,
    #     'non_downloaded_config': non_downloaded_config,
    #     'non_analyzed_layer_tarballs': non_analyzed_layer_tarballs
    # }

    bad_image_mappers = []
    non_downloaded_config_digest = None
    
    with open(os.path.join(dest_dir[0]['job_list_dir'], 'bad_image_mapper.json'), 'r') as f:
        _image_mappers = json.load(f)

    for _image_mapper in _image_mappers:

        non_analyzed_layer_tarballs = []

        for key, val in _image_mapper['bad_manifest'].items():
            manifest_name = key

        if _image_mapper['non_downloaded_config']:
            for key, val in _image_mapper['non_downloaded_config'].items():
                non_downloaded_config_digest = val

        if _image_mapper['non_analyzed_layer_tarballs']:
            for key, val in _image_mapper['non_analyzed_layer_tarballs'].items():
                non_analyzed_layer_tarballs.append(key)

        bad_image_mapper = {
            'bad_manifest': manifest_name,
            'non_downloaded_config_digest': non_downloaded_config_digest,
            'non_analyzed_layer_tarballs_digests': non_analyzed_layer_tarballs
        }

        bad_image_mappers.append(bad_image_mapper)
	
    print bad_image_mappers[0]

    return bad_image_mappers


def load_image_mappers():
    """load_image_mappers"""
    # image_mapper = {
    #     'version': version,
    #     'manifest': manifest_name_dir_map{},
    #     'config': config_name_dir_map{},
    #     'layers': layers_map{:{:}}
    # }

    image_mappers = []

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'image_mapper.json'), 'r') as f:
        _image_mappers = json.load(f)

    logging.debug("load image_mapper: %s", os.path.join(dest_dir[0]['job_list_dir'], 'image_mapper.json'))

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
    return image_mappers


def load_layers_mappers():
    layer_mappers = []

    # analyzed_layers = 0

    with open(os.path.join(dest_dir[0]['job_list_dir'], 'layer_mappers.json'), 'r') as f:
        _layer_mapper = json.load(f)

    for key, val in _layer_mapper.items():
        tmp_mapper = {}
        tmp_mapper[key] = val
        layer_mappers.append(tmp_mapper)

    return len(layer_mappers)
