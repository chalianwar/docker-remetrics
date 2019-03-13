
from draw_pic import *

# type = []
sha256 = []
#stat_type = []
stat_size = []


def run_plotmetrics_file_data():
    load_file_metrics_data_file()
    # try:
    #     plot_graph('type')
    # except:
    #     print "Cannot plot type", sys.exc_info()
    #     traceback.print_exc(file=sys.stdout)
    try:
        plot_graph('sha256')
    except:
        print "cannot plot sha256", sys.exc_info()
        traceback.print_exc(file=sys.stdout)
    # try:
    #     plot_graph('stat_type')
    # except:
    #     print "cannot print stat_type", sys.exc_info()
    #     traceback.print_exc(file=sys.stdout)

    try:
        plot_graph('stat_size')
    except:
        print "cannot print stat_size", sys.exc_info()
        traceback.print_exc(file=sys.stdout)


def plot_graph(type):

    print "===========> plot %s <=========="%type
    fig = fig_size('min')  # 'large'

    if type == 'stat_size':
        data1 = stat_size
        xlabel = 'File size (KB)'
        data = [x * 1.0 / 1024 for x in data1]
        xlim = 250

    elif type == 'sha256':
        data = sha256
        xlabel = 'Repeate files across all images'
        xlim = max(data)

    # elif type == 'type':
    #     data = sha256
    #     xlabel = 'Repeate file type across all images'
    #     xlim = max(data)

    print "xlim = %f, len = %d"%(xlim, len(data))
    plot_cdf(fig, data, xlabel, xlim, 0)


def load_file_metrics_data_file():
    print "load file"+os.path.join(dest_dir[0]['job_list_dir'], 'file_metrics_datas_stat_size.json')
    with open(os.path.join(dest_dir[0]['job_list_dir'], 'file_metrics_datas_stat_size.json'), 'r') as f_file_metrics_data:
        for line in f_file_metrics_data:
            stat_size.append(line)

    # type_dict = []
    # sha256_dict = []
    # stat_type_dict = []

    # with open(os.path.join(dest_dir[0]['job_list_dir'], 'repeate_file_type.json'), 'w') as f:
    #     for line in f:
    #         # type_dict[key] = val
    #         val = line.split(" ")[0]
    #         type.append(val)
    print "load file"+os.path.join(dest_dir[0]['job_list_dir'], 'file_sha256_uniq.cnt')
    with open(os.path.join(dest_dir[0]['job_list_dir'], 'file_sha256_uniq.cnt'), 'w') as f:
        for line in f:
            # sha256_dict[key] = val
            val = line.split(" ")[0]
            sha256.append(val) # repeat count
    # with open(os.path.join(dest_dir[0]['job_list_dir'], 'repeate_file_stat_type.json'), 'w') as f:
    #     for key, val in f.items():
    #         stat_type_dict[key] = val
    #         stat_type.append(val)


#def main():
 #   run_plotmetrics_image_data()


#if __name__ == '__main__':
#    print 'start!'
#    main()
#    print 'finished!'
