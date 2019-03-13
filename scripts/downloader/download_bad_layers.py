import os, sys, subprocess, select, random, urllib2, time, json, tempfile, shutil
import re
import multiprocessing
import argparse
from optparse import OptionParser
import subprocess
from collections import defaultdict
from functools import partial

dest_dirname = "/home/nannan/2tb_hdd"
dirname = dest_dirname


"""dest_dir contains three directories:
    0: root_dir
    1: manifest_dir
    2: config_dir
    3: layer_dir
    manifest_dir = os.path.join(dest_dir, "manifests")
    config_dir = os.path.join(dest_dir, "configs")
    layer_dir = os.path.join(dest_dir, "layers")
"""
dest_dir = []


def make_request(req):
    """send request to docker.io. call golang"""
    """go run down_loader.go -operation=download_blobs -repo=library/redis -tag=44888ef5307528d97578efd747ff6a5635facbcfe23c84e79159c0630daf16de  -absfilename=./test
        go run down_loader.go -operation=download_manifest -repo=library/redis -tag=latest -absfilename=./test"""

    args = "go run down_loader.go -operation=%s -repo=%s -tag=%s -absfilename=%s" % (req['operation'], req['repo_name'], req['repo_tag'], req['absfilename'])
    try:
        subprocess.check_output(args, shell=True)
    except subprocess.CalledProcessError as e:
        print e.output
        return e.output
    else:
        return None


def download_blobs(repo_name, blobs_digest, finished_layers):
    """download image blob tar files"""
    bad_layers = []
    downloaded_layers = []
    layer_states = defaultdict(list)

    for blob_digest in blobs_digest:
        if blob_digest in finished_layers:
            print "Layer Already Exist!"
            is_layer_exist = True  # need to download
        else:
            is_layer_exist = False  # dont need to download
            print "Layer Not Exist!"

        if not is_layer_exist:
            timestamp = time.time()
            filename = os.path.join(dest_dir[0]['layer_dir'], str(blob_digest).replace(':', '-') + '-' + str(timestamp))
            print filename
            str_digest = str(blob_digest).split('sha256:')
            # print str_digest
            if str_digest[1]:
                print str_digest[1]
                req = {
                    'repo_name': repo_name,
                    'repo_tag': str_digest[1],
                    'operation': 'download_blobs',
                    'absfilename': filename
                }
                error = make_request(req)
                if error:
                    bad_layers.append(blob_digest)
                    print "flush bad layer q!"
                else:
                    print "flush finished layer q!"
                    downloaded_layers.append(blob_digest)
    layer_states['bad_layers'] = bad_layers
    layer_states['downloaded_layers'] = downloaded_layers
    return layer_states


def download(layer_mappers_slices, finished_layers, finished_repos):
    #print "downloading"
    layer_states = defaultdict(list)
    for layer_mapper in layer_mappers_slices:
        for key, val in layer_mapper.items():
	    print key
            if key in finished_repos:
                print "Repo Already Exist!"
                is_repo_exist = True  #need to download
            else:
                is_repo_exist = False   #dont need to download
                print "Repo Not Exist!"

            if is_repo_exist:
                continue

            blobs_digest = list(set(val))  # remove redundant sha
            layer_states['repo_name'] = key
            layer_states['layer_states'].append(download_blobs(key, blobs_digest, finished_layers))
    return layer_states


def load_repos(filename):
    repos = []
    with open(filename) as fd:
        for name1 in fd:
            if not name1:
                continue
            name = str(name1).replace(" ", "").replace("\n", "")
            if name is None:
                continue
            if '/' not in name:
                print "This is an official repo, add library to it"
		print name
                name2 = "library/"+name
                name = name2
		print "official repo: %s"%name
            repo = {
                'name': name,
                # 'is_official': is_official_repo(name),
                # 'docker_io_http': construct_url(name, is_official_repo(name)),
                'tag': 'latest'  # here we use latest as all images tags
            }
            repos.append(repo)
            print repo
            #repos.append(repo)
    return repos
            # q.put(repo)


def load_bad_layers_mappers():
    with open(os.path.join(dest_dirname, 'job_list_dir/bad_layer_downloader_job_list.out'), 'r') as f_out:
        bad_layer_downloader_job_list = json.load(f_out)

    layer_mapper = defaultdict(list)

    for key, val in bad_layer_downloader_job_list.items():
        digests = []
        if len(val):
            for digest in val:
                digests.append(digest)
        layer_mapper[key] = digests

    return layer_mapper


def update_repo_names(repos, bad_layer_mappers):
    #keys = bad_layer_mappers.keys()
    layer_mappers = []
    for repo in repos:
        layer_mapper = {}
        name = repo['name'].replace("/", "-") + '-' + repo['tag']
	try:
	    a = bad_layer_mappers[name]
	except:
	    print "Layer Repo Already Analyzed!"
	    pass
	else:
        #if name in keys:
            print "Find A Non Analyzed Layer Repo %s: %s" % (repo['name'], name)
	    if len(bad_layer_mappers[name]):
            	layer_mapper[repo['name']] = bad_layer_mappers[name]
            	layer_mappers.append(layer_mapper)
        #else:
        #    print "Layer Repo Already Analyzed!"
    print layer_mappers[0]
    print len(layer_mappers)
    return layer_mappers


def load_finished_file(filename):
    finished_items = []
    with open(filename) as f:
        # lines = f.readlines()
    # print lines
        for line in f:
            print line
            if line:
                print line.replace("\n", "")
                finished_items.append(line.replace("\n", ""))
    return finished_items


def create_dirs(dirname, filename):
    manifest_dir = os.path.join(dirname, "manifests")#+str(filename).replace("/", "-"))
    config_dir = os.path.join(dirname, "configs")
    layer_dir = os.path.join(dirname, "layers")

    """Here, we create new manifest dir if manifest exist! and mv old manifest to manifest-timestamp"""
    if not os.path.exists(manifest_dir):
        #timestamp = time.time()
        #cmd5 = "mv %s %s" % (manifest_dir, os.path.join(dirname, "manifests-"+str(filename).replace("/", "-")+"-"+str(timestamp)))
        #rc = os.system(cmd5)
        #assert (rc == 0)
        os.makedirs(manifest_dir)
        print 'create manifest_dir: %s' % manifest_dir
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print 'create config_dir: %s' % config_dir
    else:
        print 'config_dir: %s already exists' % config_dir
    if not os.path.exists(layer_dir):
        os.makedirs(layer_dir)
        print 'create layer_dir: %s' % layer_dir
    else:
        print 'layer_dir: %s already exists' % layer_dir
        # load_layer_digests(layer_dir)
    dir = {
        'dirname': dirname,
        'manifest_dir': manifest_dir,
        'config_dir': config_dir,
        'layer_dir': layer_dir  # here we use latest as all images tags
    }
    dest_dir.append(dir)


def parseArg():
    parser = OptionParser()

    parser.add_option(
        '-f',
        '--filename',
        action='store',
        dest='filename',
        help="The input file which contains all the images'names"
    )
    parser.add_option(
        '-d',
        '--dirname',
        action='store',
        dest='dirname',
        help="The output directory which will contain three directories: manifests, configs, and layers"
    )
    parser.add_option(
        '-l',
        '--finished_layer_file',
        action='store',
        dest='finished_layer_file',
        help="The input file which contains already downloaded layers"
    )
    parser.add_option(
        '-r',
        '--finished_repo_file',
        action='store',
        dest='finished_repo_file',
        help="The input file which contains already downloaded repo (manifest)"
    )

    return parser.parse_args()


def main():

    options, args = parseArg()

    print 'Input file name: ', options.filename
    if not os.path.isfile(options.filename):
        print '%s is not a valid file' % options.filename
        return

    print 'Output directory: ', options.dirname
    if not os.path.isdir(options.dirname):
        print '%s is not a valid directory' % options.dirname
        return

    if options.finished_layer_file:
        print 'finished layer file: ', options.finished_layer_file
        if not os.path.isfile(options.finished_layer_file):
            print '%s is not a valid file' % options.finished_layer_file
            return
        _finished_layers = load_finished_file(options.finished_layer_file)

    if options.finished_repo_file:
        print 'finished repo file: ', options.finished_repo_file
        if not os.path.isfile(options.finished_repo_file):
            print '%s is not a valid file' % options.finished_repo_file
            return
        _finished_repos = load_finished_file(options.finished_repo_file)

    create_dirs(options.dirname, options.filename)

    repos = load_repos(options.filename)
    start = time.time()

    #logging.info('=============> run_getmetricsdata <===========')

    bad_layer_mappers = load_bad_layers_mappers()

    layer_mappers = update_repo_names(repos, bad_layer_mappers)

    print "create pool"
    P2 = multiprocessing.Pool(60)
    print "before map"

    func = partial(download, finished_layers=_finished_layers, finished_repos= _finished_repos)

    layer_mappers_slices = [layer_mappers[i:i + 24] for i in range(0, len(layer_mappers), 24)]
    print len(layer_mappers_slices)
    layer_states = P2.map(func, layer_mappers_slices)

    print "after map"

    bad_layers = []
    downloaded_layers = []

    for layer_state in layer_states:
        if len(layer_state['layer_states']):
            for layer_status in layer_state['layer_states']:
                bad_layers = layer_status['bad_layers']
                downloaded_layers = layer_status['downloaded_layers']

    with open(os.path.join(dest_dirname, 'job_list_dir/bad_repo_list.out'), 'a+') as f_bad_repo_list:
        for bad_layer_digest in bad_layers:
            f_bad_repo_list.write(bad_layer_digest+'\n')
    with open(options.finished_layer_file, 'a+') as f_out:
        for layer_digest in downloaded_layers:
            f_out.write(layer_digest+'\n')

    """close files"""
    elapsed = time.time() - start
    print (elapsed / 3600)


if __name__ == '__main__':
    main()
    print 'should exit here!'
    exit(0)


