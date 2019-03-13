
from config import *


def create_job_list():
    job_list_dir = dest_dir[0]['job_list_dir']

    tarballs = {}
    logging.debug("=================> create job list <==============\n loading layer dir %s waiting~10 min to start ......", 
	dest_dir[0]['layer_dir'])
    for path, _, tarball_filenames in os.walk(dest_dir[0]['layer_dir']):
        for tarball_filename in tarball_filenames:
	    print tarball_filename
            f_size = os.lstat(os.path.join(path, tarball_filename)).st_size
            tarballs[tarball_filename] = f_size
            logging.debug('layer_tarball: %s, size %d', tarball_filename, f_size)

    #d_ascending = OrderedDict(sorted(tarballs.items(), key=lambda kv: kv[1]))
    #logging.debug(d_ascending)

    #list_50mb = os.path.join(job_list_dir, 'list_less_50m.out')
    #with open(list_50mb, 'w+') as f_out:
    #    tmp_dict = {key: val for key, val in tarballs.items() if val <= 50*1024*1024}
    #    json.dump(tmp_dict, f_out)

    #list_1gb = os.path.join(job_list_dir, 'list_less_1g.out')
    #with open(list_1gb, 'w+') as f_out:
    #    tmp_dict = {key: val for key, val in tarballs.items() if val > 50*1024*1024 and val <= 1024*1024*1024}
    #    json.dump(tmp_dict, f_out)

    #list_2gb = os.path.join(job_list_dir, 'list_less_2g.out')
    #with open(list_2gb, 'w+') as f_out:
    #    tmp_dict = {key: val for key, val in tarballs.items() if val > 1024*1024*1024  and val <= 2*1024*1024*1024}
    #    json.dump(tmp_dict, f_out)

    list_b_2gb = os.path.join(job_list_dir, 'list_less_4g.out')
    with open(list_b_2gb, 'w+') as f_out:
        tmp_dict = {key: val for key, val in tarballs.items() if val > 2*1024*1024*1024 and val <= 4*1024*1024*1024}
        json.dump(tmp_dict, f_out)

    list_b_2gb = os.path.join(job_list_dir, 'list_less_8g.out')
    with open(list_b_2gb, 'w+') as f_out:
        tmp_dict = {key: val for key, val in tarballs.items() if val > 4*1024*1024*1024 and val <= 8*1024*1024*1024}
        json.dump(tmp_dict, f_out)

    list_b_2gb = os.path.join(job_list_dir, 'list_less_10g.out')
    with open(list_b_2gb, 'w+') as f_out:
        tmp_dict = {key: val for key, val in tarballs.items() if val > 8*1024*1024*1024 and val <= 10*1024*1024*1024}
        json.dump(tmp_dict, f_out)

    list_b_2gb = os.path.join(job_list_dir, 'list_less_14g.out')
    with open(list_b_2gb, 'w+') as f_out:
        tmp_dict = {key: val for key, val in tarballs.items() if val > 10*1024*1024*1024 and val <= 14*1024*1024*1024}
        json.dump(tmp_dict, f_out)

    list_b_2gb = os.path.join(job_list_dir, 'list_less_20g.out')
    with open(list_b_2gb, 'w+') as f_out:
        tmp_dict = {key: val for key, val in tarballs.items() if val > 14*1024*1024*1024 and val <= 20*1024*1024*1024}
        json.dump(tmp_dict, f_out)

    list_b_2gb = os.path.join(job_list_dir, 'list_bigger_20g.out')
    with open(list_b_2gb, 'w+') as f_out:
        tmp_dict = {key: val for key, val in tarballs.items() if val > 20*1024*1024*1024}
        json.dump(tmp_dict, f_out)



