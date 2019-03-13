
# import sys
# sys.path.append('../libraries/')
# from config import *
# from draw_pic import *
from get_metrics_image_data import *
from get_metrics_layer_data import *
#from get_metrics_file_data_each import *
from generate_job_list import *
#from parse_metrics_data_to_files import *
#from plot_metrics_image_data import *
#from plot_metrics_layer_data import *
#from plot_metrics_file_data import *
# from plot_graph import *


def parseArg():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-D', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.INFO,
    )

    parser.add_argument(
        '-I', '--getmetrics_image_data',
        help="get metrics image data",
        action="store_true",  # dest="loglevel", const=logging.INFO,
    )

    parser.add_argument(
        '-L', '--getmetrics_layer_data',
        help="get metrics layer data",
        action="store_true",  # dest="loglevel", const=logging.INFO,
    )

#    parser.add_argument(
#        '-F', '--getmetrics_file_data',
#        help="get metrics file data",
#        action="store_true",  # dest="loglevel", const=logging.INFO,
#    )

    parser.add_argument(
        '-J', '--generatejoblist',
        help="generate analyzer job list",
        action="store_true",  # dest="loglevel", const=logging.INFO,
    )

#    parser.add_argument(
#        '-i', '--plotgraph_image',
#        help="plot image graphs",
#        action="store_true",  # dest="loglevel", const=logging.INFO,
#    )
#
#    parser.add_argument(
#        '-l', '--plotgraph_layer',
#        help="plot layer graphs",
#        action="store_true",  # dest="loglevel", const=logging.INFO,
#    )
#
#    parser.add_argument(
#        '-f', '--plotgraph_file',
#        help="plot file graphs",
#        action="store_true",  # dest="loglevel", const=logging.INFO,
#    )
#
#    parser.add_argument(
#        '-p', '--parsemetrics_data',
#        help="plot file graphs",
#        action="store_true",  # dest="loglevel", const=logging.INFO,
#    )

    return parser.parse_args()


def main():
    args = parseArg()
    print args
    #logging.basicConfig(level=args.loglevel)
    fmt="%(funcName)s():%(lineno)i: %(message)s %(levelname)s"
    logging.basicConfig(level=args.loglevel, format=fmt)
    load_config()

    if args.getmetrics_image_data:
        run_getmetrics_image_data()

    if args.getmetrics_layer_data:
        run_getmetrics_layer_data()

    if args.getmetrics_file_data:
        run_getmetrics_file_data()

    if args.generatejoblist:
        run_generatejoblist()

#    if args.plotgraph_image:
#        run_plotmetrics_image_data()
#
#    if args.plotgraph_layer:
#        run_plotmetrics_layer_data()
#
#    if args.plotgraph_file:
#        run_plotmetrics_file_data()
#
#    if args.parsemetrics_data:
#        run_parsemetrics_data()


if __name__ == '__main__':
    print 'start!'
    main()
    print 'finished!'

