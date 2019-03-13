
from config import *

layer_json_map_dir = {}
manifest_map_dir = {}
layer_config_map_dir = {}

def load_dir(abs_dirname):
    for filename in os.listdir(abs_dirname):
        abs_filename = os.path.join(abs_dirname, filename)
        if os.path.isfile(abs_filename):
            #if '/' in filename:
            #    extract_manifest_name(filename, abs_filename) 
            if filename.startswith('sha256-') and len(filename) >= 82:
                if 'json' not in filename:
                    extract_layer_config_name(filename, abs_filename)
                else:
                    extract_layer_json_name(filename, abs_filename)
            else:
                extract_manifest_name(filename, abs_filename)

def extract_manifest_name(filename, abs_filename):
    #sstr = filename.split("-")
    name = filename.rsplit('-', 1)[0]
    print "manifest: name: %s, abs_filename: %s"%(name, abs_filename)
    manifest_map_dir[name] = abs_filename
    #f.write(abs_filename+'\n')

def extract_layer_config_name(filename, abs_filename):
    sstr = filename.split("-")
    name = "sha256:"+sstr[1]
    print "layer or config: name: %s, abs_filename: %s"%(name, abs_filename)
    layer_config_map_dir[name] = abs_filename

def extract_layer_json_name(filename, abs_filename):
        sstr = filename.split("-")
        name = "sha256:"+sstr[1]
        print "layer json file: name: %s, abs_filename: %s"%(name, abs_filename)
        layer_json_map_dir[name] = abs_filename

def list_dir_files():
    for dir in dirs:
        load_dir(dir)
    if manifest_map_dir:
        with open(os.path.join(dest_dir[0]['job_list_dir'], manifest_map_dir_filename), 'w') as f:
            json.dump(manifest_map_dir, f)
    if layer_config_map_dir:
        with open(os.path.join(dest_dir[0]['job_list_dir'], layer_config_map_dir_filename), 'w') as f:
            json.dump(layer_config_map_dir, f)
    if layer_json_map_dir:
        with open(os.path.join(dest_dir[0]['job_list_dir'], layer_json_map_dir_filename), 'w') as f:
            json.dump(layer_json_map_dir, f)

# if __name__ == '__main__':
#     print 'start!'
#     main()
#     print 'finished!'
