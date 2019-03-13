
import os, json, multiprocessing#,logging


manifest_names = []
dest_dirname = "/home/nannan/2tb_hdd/job_list_dir/"
manifest_map_dir = {}
manifest_map_dir_filename = "manifest_map_dir.json"

# layer_json_map_dir = {}
# layer_config_map_dir = {}


def manifest_schemalist(manifest):
    blobs_digest = []
    if 'manifests' in manifest and isinstance(manifest['manifests'], list) and len(manifest['manifests']) > 0:
        for i in manifest['manifests']:
            if 'digest' in i:
                #print i['digest']
                blobs_digest.append(i['digest'])
    return blobs_digest


def manifest_schema2(manifest, r_type):
    blobs_digest = []
    if r_type == 'config':
        if 'config' in manifest and 'digest' in manifest['config']:
            config_digest = manifest['config']['digest']
            blobs_digest.append(config_digest)
            return blobs_digest
    elif r_type == 'layers':
        if 'layers' in manifest and isinstance(manifest['layers'], list) and len(manifest['layers']) > 0:
            for i in manifest['layers']:
                if 'digest' in i:
                    #print i['digest']
                    blobs_digest.append(i['digest'])
            return blobs_digest
    else:
        print "################## which one to load? config or layers ##################"


def manifest_schema1(manifest):
    blobs_digest = []
    if 'fsLayers' in manifest and isinstance(manifest['fsLayers'], list) and len(manifest['fsLayers']) > 0:
        for i in manifest['fsLayers']:
            if 'blobSum' in i:
                #print i['blobSum']
                blobs_digest.append(i['blobSum'])
    return list(set(blobs_digest)) # blobs_digest


def process_manifest(manifest_filename):
    blobs_digest = []
    config_digest = []
    # bad_manifest = {}
    json_data = {}

    print "process manifest_filename: %s, abs_name: %s"%(manifest_filename, manifest_map_dir[manifest_filename])
    manifest_absfilename = manifest_map_dir[manifest_filename]
    if not os.path.isfile(manifest_absfilename):
        print "#################### manifest: %s is not a valid file! ####################"%manifest_absfilename
        return {}
    with open(manifest_absfilename) as f:
        try:
            manifest_json_data = json.load(f)
        except:
            print "except: cannot load-manifest: manfiest: %s; config: %s"%(manifest_filename, manifest_absfilename)
            # bad_manifest[manifest_filename] = manifest_absfilename
            json_data['bad_manifest'] = manifest_absfilename
            print json_data
            return json_data            

    if 'schemaVersion' in manifest_json_data and manifest_json_data['schemaVersion'] == 2:
        if 'mediaType' in manifest_json_data and 'list' in manifest_json_data['mediaType']:
            blobs_digest = manifest_schemalist(manifest_json_data)
            version = 'schemalist'
        else:
            config_digest = manifest_schema2(manifest_json_data, 'config')
            blobs_digest = manifest_schema2(manifest_json_data, 'layers')
            version = 'schema2'
            #print('config_digest:%s; blobs_digests: %s; version: %s'% (config_digest, blobs_digest, version))
    elif 'schemaVersion' in manifest_json_data and manifest_json_data['schemaVersion'] == 1:
        blobs_digest = manifest_schema1(manifest_json_data)
        version = 'schema1'
        #print('blobs_digests: %s, version: %s'% (blobs_digest, version))

    # # manifest_name_dir_map = {}
    # # config_name_dir_map = {}
    # # layers_map = {}
    # # non_downloaded_config = {}
    # # non_analyzed_layer_tarballs = {}
    #
    # # manifest_name_dir_map[manifest_filename] = manifest_absfilename
    # if config_digest:
     #    try:
     #        layer_config_map_dir[config_digest[0]]
     #    except:
     #        """write to non-downloaded-configs.json: manfiest name and config digest"""
     #        print "except: non-downloaded-config: manfiest: %s; config: %s"%(manifest_filename, config_digest[0])
     #        non_downloaded_config['non_downloaded_config_digest'] = config_digest[0]
	# else:
     #        config_name_dir_map[config_digest[0]] = layer_config_map_dir[config_digest[0]]
    # if not blobs_digest:
     #    non_analyzed_layer_tarballs['non_blobs_in_manifest'] = True
    # else:
    	# for layer_digest in blobs_digest:
     #        layer_name_dir_map = {}
    #
     #        try:
     #        	layer_json_map_dir[layer_digest]
     #        except:
     #        	"""write to non-analyzed-layers.json: manifest name and layer digest"""
     #        	print "except: non-analyzed-layertarball: manfiest: %s; layer_digest: %s"%(manifest_filename, layer_digest)
     #        	non_analyzed_layer_tarballs[layer_digest] = True
     #        else:
     #        	layer_name_dir_map['json_absfilename'] = layer_json_map_dir[layer_digest]
     #        	layers_map[layer_digest] = layer_name_dir_map
    #
    # #if non_analyzed_layer_tarballs:
    # bad_image_mapper = {
     #    'version': version,
     #    'bad_manifest': manifest_name_dir_map,
     #    'non_downloaded_config': non_downloaded_config,
     #    'non_analyzed_layer_tarballs': non_analyzed_layer_tarballs
    # }
    #
    # json_data['bad_image_mapper'] = bad_image_mapper
    # # return json_data
    # has_non_analyzed_layer_tarballs = False
    # has_non_downloaded_config = False
    #
    # if non_analyzed_layer_tarballs:
	# has_non_analyzed_layer_tarballs = True
    # if non_downloaded_config:
	# has_non_downloaded_config = True

    image_mapper = {
        'version': version,
        'manifest': manifest_filename,
        'config': config_digest,
        'layers': blobs_digest,
	# 'has_non_analyzed_layer_tarballs': has_non_analyzed_layer_tarballs,
	# 'has_non_downloaded_config': has_non_downloaded_config
    }

    json_data['image_mapper'] = image_mapper

    """write to image_mapper.json: image_mapper"""
    #print json_data
    return json_data


def load_all_map_dir(manifest_map_dir):
    with open(os.path.join(dest_dirname, manifest_map_dir_filename)) as f:
        _manifest_map_dir = json.load(f)
    for key, val in _manifest_map_dir.items():
        manifest_map_dir[key] = val
    # with open(image_names_absfilename, 'r') as f:
    # repos = []
    # with open(image_names_absfilename) as fd:
    #     for name1 in fd:
    #         if not name1:
    #             continue
    #         name = str(name1).replace(" ", "").replace("\n", "")
    #         if name is None:
    #             continue
    #         if '/' not in name:
    #             print "This is an official repo, add library to it"
    #             print name
    #             name2 = "library/" + name
    #             name = name2
    #             print "official repo: %s" % name
    #         repo = {
    #             'name': name,
    #             # 'is_official': is_official_repo(name),
    #             # 'docker_io_http': construct_url(name, is_official_repo(name)),
    #             'tag': 'latest'  # here we use latest as all images tags
    #         }
    #         # repos.append(repo)
    #         print repo
    #         repos.append(repo)
    #         return repos

    #manifest_names = list(manifest_map_dir.keys())
    for i in manifest_map_dir.keys():
        manifest_names.append(i)
    print "manifest_names: %s"%manifest_names
    # with open(os.path.join(dest_dir[0]['job_list_dir'],layer_json_map_dir_filename)) as f:
    #     _layer_json_map_dir = json.load(f)
    # for key, val in _layer_json_map_dir.items():
    #     layer_json_map_dir[key] = val
    #
    # with open(os.path.join(dest_dir[0]['job_list_dir'],layer_config_map_dir_filename)) as f:
    #     _layer_config_map_dir = json.load(f)
    # for key, val in _layer_config_map_dir.items():
    #     layer_config_map_dir[key] = val


def write_json_datas(json_datas):
    image_mappers = []
    # bad_manifest = []
    bad_manifest = []
    for json_data in json_datas:
        if 'bad_manifest' in json_data:
            bad_manifest.append(json_data['bad_manifest'])
        if 'image_mapper' in json_data:
            image_mappers.append(json_data['image_mapper'])

    """write image mapper"""
    if image_mappers:
        with open(os.path.join(dest_dirname,'imagename_mapper_digests.json'), 'w') as f:
            json.dump(image_mappers, f)
    if bad_manifest:
        with open(os.path.join(dest_dirname,'bad_image_manifest.json'), 'w') as f:
            json.dump(bad_manifest, f)


def create_image_mapper():
    """create image mapper as a json file"""
    print('=============> create_image_mapper: create image mapper {repo_name: digest list} <===========')
    load_all_map_dir(manifest_map_dir)
    print "create pool"
    P = multiprocessing.Pool(60)
    print "before map!"
    print len(manifest_names) #process_manifest
    # print len(layer_json_map_dir)
    # print "before map!"
    #json_datas = []
    #for i in manifest_names:
    #	json_datas.append(process_manifest(i))
    json_datas = P.map(process_manifest, manifest_names)
    print "after map"
    print "write to files!"
    write_json_datas(json_datas)
    

if __name__ == '__main__':
   print 'start!'
   create_image_mapper()
   print 'finished!'
