
from run_funcs import *
from utilities_funcs import *


""" TODO:
    1. put layer json to a single file
     2. fetch all the manifest
     3. get all the tags
"""
""" python main.py -D -L -d dest_dir -a analyzed_layer_file -e extracting_dir -z zip_archival_dir"""
""" python main.py -D -I -d dest_dir -a analyzed_layer_file """


def parseArg():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-D', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.INFO,
    )

    parser.add_argument(
        '-L', '--createlayerdb',
        help="Create layer json (database)",
        action="store_true",  # dest="loglevel", const=logging.INFO,
    )

    parser.add_argument(
        '-I', '--createimagedb',
        help="Create image json (database)",
        action="store_true",  # dest="loglevel", const=logging.INFO,
    )

    parser.add_argument(
        '-J', '--jobdivider',
        help="divide the layers into job lists",
        action="store_true",  # dest="loglevel", const=logging.INFO,
    )

    parser.add_argument(
        '-F', '--listdirfiles',
        help="list the directories files",
        action="store_true",  # dest="loglevel", const=logging.INFO,
    )

    return parser.parse_args()


def main():
    args = parseArg()
    print args
    #logging.basicConfig(level=args.loglevel)
    fmt="%(funcName)s():%(lineno)i: %(message)s %(levelname)s"
    logging.basicConfig(level=args.loglevel, format=fmt)
    load_config()

    if args.createlayerdb:
        run_createlayerdb()

    if args.createimagedb:
        run_createimagedb()

    if args.jobdivider:
        run_jobdivider()

    if args.listdirfiles:
        run_listdirfiles()


if __name__ == '__main__':
    print 'start!'
    main()
    print 'finished!'
