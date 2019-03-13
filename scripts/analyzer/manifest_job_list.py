
from config import *
#import os, json
from utilities_funcs import *

unique_image_list_filename = "../downloader/image_names.list"
manifest_jobs = []
manifest_jobs_filename = "To_download_images-key.list"
image_list = []
image_map = {}
#downloaded_manifest_map = {}

def manifest_job_list():
    load_config()
    with open(os.path.join(dest_dir[0]['job_list_dir'], manifest_map_dir_filename)) as f:
        manifest_map_dir = json.load(f)
	#for key, value in manifest_map_dir.items():
	#     downloaded_manifest_map[key] = value

    manifest_list = manifest_map_dir.keys()
    print manifest_list

    with open(unique_image_list_filename) as fd:
        for name1 in fd:
            if not name1:
                continue
            name = str(name1).replace(" ", "").replace("\n", "")
            if name is None:
                continue
            if '/' not in name:
                print "This is an official repo, add library to it"
            	print name
            	name2 = "library/" + name
            	name = name2
            	print "official repo: %s" % name
	    repo_name = name
            name3 = name.replace("/", "-")
	    name4 = name3+"-latest"
	    name = name4
	    image_list.append(name)
	    image_map[name] = repo_name

    print image_list
    #return
    for key in image_list:
	try:
	    repo_path = manifest_map_dir[key]
        #if key in manifest_list:
            print "Downloaded %s"%key
        except:
            print "Not downloaded %s"%key
            manifest_jobs.append(image_map[key])
    print manifest_jobs

    with open(manifest_jobs_filename, 'w') as f:
        for i in manifest_jobs:
            f.write(i+"\n")


if __name__ == '__main__':
    print 'start!'
    manifest_job_list()
    print 'finished!'
