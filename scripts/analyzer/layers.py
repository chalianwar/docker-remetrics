
from config import *
from dir import *


"""TODO:
    # 1. check duplicated.
    # 2. mount tmpfs
    # 3. already has json file no need to extracting again
    1. need to add more remetrics 
    2. remove layer db json timestamp
"""

analyzed_layer_list = []
layer_job_list = []


def create_layer_db():
    """create layer database as a json file"""
    logging.info('=============> create_layer_db: create layer metadata json files <===========')
    analyzed_layer_filename = analyzed_absfilename
    layer_list_filename = layer_list_absfilename

    queue_layers(analyzed_layer_filename, layer_list_filename)

    print "create pool"
    P = multiprocessing.Pool(num_worker_process)
    print "before map!"
    print len(layer_job_list)  # process_manifest
    print len(analyzed_layer_list)
    print "before map!"
   # for i in layer_job_list:
   #     if not i:
   #         continue
   #     process_layer(i)
   #     break
    json_datas = P.map(process_layer, layer_job_list)
    print "after map"

    logging.info('done! all the layer job processes are finished')


def queue_layers(analyzed_layer_filename, layer_list_filename):
    """queue the layer id in layer_list_filename, layer id = sha256-digest with timestamp"""
    num = 0
    with open(layer_list_filename) as f:
        content = json.load(f)
        for key, val in content.items():
            logging.debug('queue dir layer tarball: %s', key)  #
	    #num = num + 1
	    #if num > 50:
            #    break
            layer_job_list.append(key)

    """queue the layer id in analyzed_layer_filename, layer id = sha256:digest !!! without timestamp"""
    num = 0
    with open(analyzed_layer_filename) as f:
        for line in f:
            print line
	    #num = num + 1
	    #if num > 50:
		#break
            if line:
                logging.debug('queue layer_id: %s to analyzed_layer_queue', line.replace("\n", ""))  #
                analyzed_layer_list.append(line.replace("\n", ""))


def check_file_type(filename):
    tarball_filename = os.path.join(dest_dir[0]['layer_dir'], filename)
    cmd2 = 'file %s' % tarball_filename
    logging.debug('The shell command: %s', cmd2)

    proc = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    logging.debug('The shell output: %s', out)
    if 'gzip' in out:
        return 'gzip'
    elif 'tar' in out:
        return 'tar'
    else:
        return None


def process_layer(layer_filename):
    processname = multiprocessing.current_process().name
    logging.debug("[%s] process layer_filename: %s", processname, layer_filename)

    layer_db_json_dir = dest_dir[0]['layer_db_json_dir']

    if layer_filename is None:
        logging.debug('The layer queue is None!')
        return

    if "sha256-" not in layer_filename:
        logging.info('file %s is not a layer tarball or config file', layer_filename)
        return False
    if len(layer_filename.split("-")) != 3:
        logging.debug('The layer filename is invalid %s!', layer_filename)
        return False

    logging.info('sha256:' + layer_filename.split("-")[1])

    if ('sha256:' + layer_filename.split("-")[1]) in analyzed_layer_list:
        print "Layer Already Analyzed!"
        is_layer_analyzed = True
    else:
        is_layer_analyzed = False
        print "Layer Not Analyzed!"

    if is_layer_analyzed:
        return

    if not os.path.isfile(os.path.join(dest_dir[0]['layer_dir'], layer_filename)):
        logging.info('file %s is not valid', layer_filename)
        return False

    start = time.time()
    filetype = check_file_type(layer_filename)
    if filetype == 'tar':
        print "This is a tar file"
        archival_size = os.lstat(os.path.join(dest_dir[0]['layer_dir'], layer_filename)).st_size
        logging.debug("archival_size %d B, name: %s", archival_size, layer_filename)
        sub_dirs, compressed_size_with_method_gzip = load_dirs(layer_filename, filetype)
        elapsed = time.time() - start
        logging.info('process directory: decompression plus sha digest calculation, consumed time ==> %f ; %d', elapsed,
                     archival_size)
    elif filetype == 'gzip':
        print "This is a gzip file"
        compressed_size_with_method_gzip = os.lstat(os.path.join(dest_dir[0]['layer_dir'], layer_filename)).st_size
        logging.debug("compressed_size_with_method_gzip %d B, name: %s", compressed_size_with_method_gzip, layer_filename)
        sub_dirs, archival_size = load_dirs(layer_filename, filetype)
        elapsed = time.time() - start
        logging.info('process directory: decompression plus sha digest calculation, consumed time ==> %f ; %d', elapsed,
                     compressed_size_with_method_gzip)
    else:
        logging.info('################### The layer tarball type is neither tar or gzip! layer file name %s ###################', layer_filename)
        return

    if not len(sub_dirs):
        """"write to bad layer_tarball"""
        with open("bad_nonanalyzed_layer_list-%s.out" % processname, 'a+') as f:
            f.write(layer_filename+'\n')
        logging.debug('################### The layer tarball has problems! layer file name %s ###################', layer_filename)
        return

    if archival_size == -1 or compressed_size_with_method_gzip == -1:
        return

    depths = [sub_dir['dir_depth'] for sub_dir in sub_dirs if sub_dir]
    dir_depth = {
        'dir_max_depth': max(depths),
        'dir_min_depth': min(depths),
        'dir_median_depth': statistics.median(depths),
        'dir_avg_depth': statistics.mean(depths)
    }

    sha, id, timestamp = str(layer_filename).split("-")

    size = {
        'uncompressed_sum_of_files': sum_layer_size(sub_dirs),
        'compressed_size_with_method_gzip': compressed_size_with_method_gzip,
        'archival_size': archival_size   # archival_size
    }

    layer = {
        'layer_id': sha+':'+id,  # str(layer_id).replace("/", ""),
        'dirs': sub_dirs,  # getLayersBychainID(chain_id),
        'layer_depth': dir_depth,
        'size': size,  # sum of files size,
        'repeats': 0,
        'file_cnt': sum_file_cnt(sub_dirs)
    }

    abslayer_filename = os.path.join(layer_db_json_dir, layer_filename+'.json')
    logging.info('write to layer json file: %s', abslayer_filename)
    with open(abslayer_filename, 'w+') as f_out:
        json.dump(layer, f_out)

    logging.debug('write layer_id:[%s]: to json file %s', layer_filename, abslayer_filename)

    with open("analyzed_layer_filename-%s.out" % processname, 'a+') as f:
        f.write(layer_filename + '\n')


# def flush_file(fd, q_name, lock_file):
#     while True:
#         item = q_name.get()
#         if item is None:
#             print str(q_name) + " queue empty!"
#             break
#         """write to file"""
#         print "f_finished_item: " + item
#         with lock_file:
#             fd.write(item + "\n")
#             fd.flush()
#         q_name.task_done()


def sum_layer_size(sub_dirs):
    sum = 0
    for dir in sub_dirs:
        sum = sum + dir['dir_size']
    return sum


def sum_file_cnt(sub_dirs):
    sum = 0
    for dir in sub_dirs:
        sum = sum + dir['file_cnt']
    return sum
#
#
# def cal_layer_repeats(images):
#     """ [imge1's layers, image2's layers, ..... ]
#     get unique elements among multiple lists: all_list"""
#     #fout = open('layer-repeats.txt', 'w+')
#     layers = []
#     for image in images:
#         image_layers = []
#         for layer in image['layers']:
#             #print layer
#             diff_path = os.path.join(dest_dir['layer_dir'], layer['cache_id'])
#             logging.debug('%s', '\n'.join(diff_path))
#             """here, find all layer for each image"""
#             image_layers.append(layer['cache_id'])
#         layers.append(image_layers)
#     print layers[0]
#
#     layer_union = list(chain(*layers))
#     print layer_union[0]
#     layer_dict = {i:layer_union.count(i) for i in layer_union}
#     #layer_repeats_dict = cal_layer_repeats(images)
#     for k, v in layer_dict.items():
#         print (k, v)
#         #fout.writelines(str(k)+','+str(v)+'\n')
#         for image in images:
#             for layer in image['layers']:
#                 #print layer
#                 if layer['cache_id'] == k:
#                     layer['repeats'] = v
#                 #print layer
#
#
# def plt_repeat_layer(images):
#     d = {}
#     for image in images:
#         for layer in image['layers']:
#             if layer['repeats'] not in d:
#                 d[layer['repeats']] = []
#             d[layer['repeats']].append(layer['size'])
#             #print d
#
#     sort_layersbyrepeats = sorted(d.items())
#
#     x = []
#     y = []
#     for item in sort_layersbyrepeats:
#         print (item[0], item[1])
#         k = item[0]
#         v = item[1]
#         sum1 = sum(map(int, v))
#         x.append(int(k))
#         y.append(float(sum1)/len(v) / 1024 / 1024)
#
#     fig = fig_size('small')
#     plot_bar_pic(fig, x, y, 'Repeats', 'Average Size(MB)', max(x), max(x))
#
#     x = []
#     y = []
#     for item in sort_layersbyrepeats:
#         print (item[0], item[1])
#         k = item[0]
#         v = item[1]
#         sum1 = sum(map(int, v))
#         x.append(int(k))
#         y.append(float(sum1) / 1024 / 1024 / 1024)
#     fig = fig_size('small')
#     plot_bar_pic(fig, x, y, 'Repeats', 'Total Size(GB)', max(x), max(x))
#
#     x = []
#     y = []
#     for item in sort_layersbyrepeats:
#         print (item[0], item[1])
#         k = item[0]
#         v = item[1]
#         # sum1 = sum(map(int, v))
#         x.append(int(k))
#         y.append(len(v))
#     fig = fig_size('small')
#     plot_bar_pic(fig, x, y, 'Repeats', 'file count', max(x), max(x))

