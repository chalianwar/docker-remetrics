
import sys
sys.path.append('../libraries/')
from regular_libraries import *


"""configurations for setup"""

dest_dirname = "/home/nannan/2tb_hdd"

"""configurations for multithreading"""

num_worker_process = 20

"""contains all the global variables"""

dest_dir = []

extracting_dir = "/home/nannan/120g_ssd_j/extracting_dir/"
layer_db_json_dirname = "/home/nannan/120g_ssd_k/non-analyzed-jsons"

analyzed_absfilename = "/home/nannan/2tb_hdd/job_list_dir/analyzed_absfilename.out"
layer_list_absfilename = "/home/nannan/2tb_hdd/job_list_dir/list_less_50m.out"#test_non_analyzed_layers.json"

"""Output directories which are no need to change"""

image_db_json_dirname = 'image_db_json'
job_list_dirname = 'job_list_dir'

layer_config_map_dir_filename = "layer_config_map_dir.json"
layer_json_map_dir_filename = "layer_json_map_dir.json"
manifest_map_dir_filename = "manifest_map_dir.json"

dirs = ["/home/nannan/2tb_hdd/manifests",
        "/home/nannan/2tb_hdd/configs",
        "/home/nannan/2tb_hdd/layer_db_json",
        "/home/nannan/2tb_hdd/layer_db_json_bison02",
	    "/home/nannan/2tb_hdd/layer_db_json_bison02_1",
        "/home/nannan/2tb_hdd/layer_db_json_less_2g",
        "/home/nannan/2tb_hdd/layer_db_json_bigger_2g"]

"""files for plotting"""
#image_pop_filename = ''
#image_growth_filename = ''

# ===============================================

me = magic.Magic()
