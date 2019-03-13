import os, sys, subprocess, select, random, urllib2, time, json, tempfile, shutil
import re
import threading, Queue
import argparse
from optparse import OptionParser
#import requests
import subprocess

q = Queue.Queue()
finished_layers_q = Queue.Queue()  # finished layer queue
finished_repo_q = Queue.Queue()  # finished repo queue

bad_layer_q = Queue.Queue()  # layers that cannot be downloaded
bad_repo_q = Queue.Queue()  # repos that cannot be downloaded

flush_finished_layer_q = Queue.Queue()
flush_finished_repo_q = Queue.Queue()
flush_bad_layer_q = Queue.Queue()  # layers that cannot be downloaded
flush_bad_repo_q = Queue.Queue()  # repos that cannot be downloaded

num_worker_threads = 9
num_layer_worker_threads = 6
num_flush_threads = 6

lock = threading.Lock()
lock_repo = threading.Lock()
# flush_condition = threading.Condition()

lock_f_finished_repo = threading.Lock()
lock_f_bad_repo = threading.Lock()
lock_f_finished_layer = threading.Lock()
lock_f_bad_layer = threading.Lock()

threads = []
flush_threads = []
repos = []

# /* TODO
# 	1. add log file (store all the errors)
#
# 	2. catch exceptions (input, timeout)
# */

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


def download_manifest(repo):
    """download manifest first"""
    # url = repo['docker_io_http'] + 'manifest' + '/' + repo['tag']
    # print 'manifest url: %s' % url
    timestamp = time.time()
    filename = os.path.join(dest_dir[0]['manifest_dir'], str(repo['name']).replace("/", "-") + '-' + repo['tag'] + '-' + str(timestamp) + '.json')
    print filename
    req = {
        'repo_name': repo['name'],
        'repo_tag': repo['tag'],
        'operation': 'download_manifest',
        'absfilename': filename
    }
    make_request(req)
    if not os.path.isfile(filename):
        return None
    with open(filename) as manifest_file:
        resp = json.load(manifest_file)
    if not resp:
        return None
    else:
        """return json"""
        #print resp
        return resp


def download_blobs(repo, blobs_digest):
    """download image blob tar files"""
    # digest_list = list(set(blobs_digest))  # remove redundant sha
    while True:
        digest = blobs_digest.get()
        if digest is None:
            print "layer queue is empty"
            break
        with lock:
            if digest in finished_layers_q.queue:
                print "Layer Already Exist!"
                is_layer_exist = True
            else:
                is_layer_exist = False
                finished_layers_q.put(digest)  # !!!layers might be duplicated
                print "Layer Not Exist!"

        if not is_layer_exist:
            timestamp = time.time()
            filename = os.path.join(dest_dir[0]['layer_dir'], str(digest).replace(':', '-') + '-' + str(timestamp))
            print filename
            str_digest = str(digest).split('sha256:')
            # print str_digest
            if str_digest[1]:
                print str_digest[1]
                req = {
                    'repo_name': repo['name'],
                    'repo_tag': str_digest[1],
                    'operation': 'download_blobs',
                    'absfilename': filename
                }
                error = make_request(req)
                if error:
                    bad_layer_q.put(digest)
                    print "flush bad layer q!"
                    flush_bad_layer_q.put(digest)
                else:
                    print "flush finished layer q!"
                    flush_finished_layer_q.put(digest)
        blobs_digest.task_done()


def manifest_schemalist(manifest):
    blobs_digest = []
    if 'manifests' in manifest and isinstance(manifest['manifests'], list) and len(manifest['manifests']) > 0:
        for i in manifest['manifests']:
            if 'digest' in i:
                print i['digest']
                blobs_digest.append(i['digest'])
    return blobs_digest


def manifest_schema2(manifest):
    blobs_digest = []
    if 'config' in manifest and 'digest' in manifest['config']:
        config_digest = manifest['config']['digest']
        blobs_digest.append(config_digest)
    if 'layers' in manifest and isinstance(manifest['layers'], list) and len(manifest['layers']) > 0:
        for i in manifest['layers']:
            if 'digest' in i:
                print i['digest']
                blobs_digest.append(i['digest'])
    return blobs_digest


def manifest_schema1(manifest):
    blobs_digest = []
    if 'fsLayers' in manifest and isinstance(manifest['fsLayers'], list) and len(manifest['fsLayers']) > 0:
        for i in manifest['fsLayers']:
            if 'blobSum' in i:
                print i['blobSum']
                blobs_digest.append(i['blobSum'])
    return blobs_digest


def download():
    while True:
        repo = q.get()
        if repo is None:
            print "repo queue is empty!"
            break
        """check if this repo already downloaded"""
        #with lock_repo:
        if repo['name'] in finished_repo_q.queue:
            print "Repo Already Exist!"
            is_repo_exist = True
        else:
            is_repo_exist = False
            print "Layer Not Exist!"

        if is_repo_exist:
            q.task_done()
            continue

        manifest = download_manifest(repo)
        if manifest is None:
            bad_repo_q.put(repo['name'])
            print "flush bad repo q"
            flush_bad_repo_q.put(repo['name'])
            q.task_done()
            continue

        blobs_digest = []
        layer_threads = []
        if 'schemaVersion' in manifest and manifest['schemaVersion'] == 2:
            if 'mediaType' in manifest and 'list' in manifest['mediaType']:
                blobs_digest = manifest_schemalist(manifest)
            else:
                blobs_digest = manifest_schema2(manifest)

        elif 'schemaVersion' in manifest and manifest['schemaVersion'] == 1:
            blobs_digest = manifest_schema1(manifest)

        digest_list = list(set(blobs_digest))  # remove redundant sha
        blobs_digest_q = Queue.Queue()
        for i in digest_list:
            blobs_digest_q.put(i)
        for i in range(num_layer_worker_threads):
            t = threading.Thread(target=download_blobs, args=(repo, blobs_digest_q))
            t.start()
            layer_threads.append(t)

        blobs_digest_q.join()
        print 'layer wait here!'
        for i in range(num_layer_worker_threads):
            blobs_digest_q.put(None)
        print 'layer put here!'
        for t in layer_threads:
            t.join()
        print 'layer done here!'

        """repo is unique so ...."""
        finished_repo_q.put(repo['name'])
        print "flush finished repo q"
        flush_finished_repo_q.put(repo['name'])

        q.task_done()


#def get_image_names(name):
#    """process image file list and store the names in a file"""
#    cmd1 = 'cp %s image-list.xls' % name
#    cmd2 = 'awk -F\'' + ',' + '\' \'{print $3}\' image-list.xls > image-names.xls'
#    print cmd1
#    print cmd2
#    rc = os.system(cmd1)
#    assert (rc == 0)
#    rc = os.system(cmd2)
#    assert (rc == 0)


def queue_names(filename):
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
            q.put(repo)


def load_finished_file(filename, q_name):
    with open(filename) as f:
        # lines = f.readlines()
    # print lines
        for line in f:
            print line
            if line:
                print line.replace("\n", "")
                q_name.put(line.replace("\n", ""))


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


def flush_file(fd, q_name, lock_file):
    while True:
        item = q_name.get()
        if item is None:
            print str(q_name) + "queue empty!"
            break
        """write to file"""
        print "f_finished_item: " + item
        with lock_file:
            fd.write(item + "\n")
            fd.flush()
        q_name.task_done()


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
        load_finished_file(options.finished_layer_file, finished_layers_q)

    if options.finished_repo_file:
        print 'finished repo file: ', options.finished_repo_file
        if not os.path.isfile(options.finished_repo_file):
            print '%s is not a valid file' % options.finished_repo_file
            return
        load_finished_file(options.finished_repo_file, finished_repo_q)

    #get_image_names(options.filename)
    create_dirs(options.dirname, options.filename)

    f_finished_repo = open(options.finished_repo_file, 'a+')
    f_bad_repo = open("bad_repo_list.out", 'a+')
    f_finished_layer = open(options.finished_layer_file, 'a+')
    f_bad_layer = open("bad_layer_list.out", 'a+')

    queue_names(options.filename)
    start = time.time()
    for i in range(num_worker_threads):
        t = threading.Thread(target=download)
        t.start()
        threads.append(t)

    for j in range(num_flush_threads):
        t1 = threading.Thread(target=flush_file, args=(f_finished_repo, flush_finished_repo_q, lock_f_finished_repo))
        t2 = threading.Thread(target=flush_file, args=(f_finished_layer, flush_finished_layer_q, lock_f_finished_layer))
        t3 = threading.Thread(target=flush_file, args=(f_bad_repo, flush_bad_repo_q, lock_f_bad_repo))
        t4 = threading.Thread(target=flush_file, args=(f_bad_layer, flush_bad_layer_q, lock_f_bad_layer))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        flush_threads.append(t1)
        flush_threads.append(t2)
        flush_threads.append(t3)
        flush_threads.append(t4)

    q.join()
    print 'wait here!'
    for i in range(num_worker_threads):
        q.put(None)
    print 'put here!'
    for t in threads:
        t.join()
    print 'done here!'

    flush_finished_repo_q.join()
    flush_finished_layer_q.join()
    flush_bad_repo_q.join()
    flush_bad_layer_q.join()

    print "flush queues wait here!"
    for i in range(num_flush_threads):
        flush_finished_repo_q.put(None)
        flush_finished_layer_q.put(None)
        flush_bad_repo_q.put(None)
        flush_bad_layer_q.put(None)
    for t in flush_threads:
        t.join()

    """close files"""
    elapsed = time.time() - start
    print (elapsed / 3600)


if __name__ == '__main__':
    main()
    print 'should exit here!'
    exit(0)


