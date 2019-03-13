
from contruct_image_mapper import *
from layers import *
from jobdivider import *
from list_dir_files import *


def run_createimagedb():
    start = time.time()

    create_image_db()

    elapsed = time.time() - start
    logging.info('created image json files, consumed time ==> %f', (elapsed / 3600))


def run_createlayerdb():
    start = time.time()

    logging.info('analyzed_layer_file is: %s', analyzed_absfilename)
    if not os.path.isfile(analyzed_absfilename):
        logging.error('%s is not a valid file', analyzed_absfilename)
        return

    logging.info('layer_list_file is: %s', layer_list_absfilename)
    if not os.path.isfile(layer_list_absfilename):
        logging.error('%s is not a valid file', layer_list_absfilename)
        return

    create_layer_db()

    elapsed = time.time() - start
    logging.info('created layer json files, consumed time ==> %f', (elapsed / 3600))


def run_jobdivider():
    start = time.time()

    create_job_list()

    elapsed = time.time() - start
    logging.info('created job list files, consumed time ==> %f', (elapsed / 3600))


def run_listdirfiles():
    start = time.time()

    list_dir_files()

    elapsed = time.time() - start
    logging.info('created job list files, consumed time ==> %f', (elapsed / 3600))
