
import sys
sys.path.append('../libraries/')
sys.path.append('../analyzer/')
from graph_related_libraries import *
# from regular_libraries import *
# from config import *
from utilities_funcs import *

def fig_size(size):
    if size == 'min':
	fig = plt.figure(figsize=(12, 8), dpi=80)
    if size == 'small':
	fig = plt.figure(figsize=(20, 6), dpi=80)
    if size == 'median':
        fig = plt.figure(figsize=(48, 16), dpi=80)
    elif size == 'large':
        fig = plt.figure(figsize=(128, 16), dpi=80)
    return fig


def bar_label_text(ax, x, y, xlim):
    for a, b in zip(x, y):
        if a > xlim:
            break
        if isinstance(b, int):
            ax.text(a, b + 0.05, '%d' % b)
        else:
            ax.text(a, b + 0.05, '%.1f' % b)


""" only plot the cdf """
def plot_cdf_normal(fig, data1, xlabel, xlim, ticks, y_type):
    data = np.array(data1)
    print("plot: min = %d" % data.min())
    print("plot: max = %d" % data.max())
    print("plot: median = %d" % np.median(data))

    ax = fig.add_subplot(111)

    bins = np.arange(np.ceil(data.min()), np.floor(data.max()))
    print "cdf and pdf calculating: bins = %d" % len(bins)
    counts_cdf, base_cdf = np.histogram(data, bins=bins, normed=True)

    cdf = np.cumsum(counts_cdf)

    print "start plotting!"

    cd = ax.plot(base_cdf[1:], [x*100 for x in cdf], 'b-', linewidth=1, label='Cumulative Distribution')

    print "start labeling!"

    ax.set_xlim(xmin=1, xmax=xlim)
    ax.set_ylim(0, 1*100)

    ax.set_xlabel(xlabel, fontsize=24)
    ax.set_ylabel('Cumulative % of '+y_type, fontsize=24) #24,>14
    ax.get_yaxis().set_tick_params(labelsize = 24)
    ax.get_xaxis().set_tick_params(labelsize = 24)

    plt.grid()
    name = '%s.png' % xlabel.replace(" ", "_").replace("/", "divided_by").replace(":", "")
    fig.savefig(name)


"""plot two lines: pdf and cdf"""
def plot_cdf(fig, data1, xlabel, xlim, ticks, y_type):
    data0 = np.array(data1)    
    data = data0[data0 != np.array(None)]
    #data = np.array(data)
    print("plot: min = %d" % data.min())
    print("plot: max = %d" % data.max())
    print("plot: median = %d" % np.median(data))

    ax = fig.add_subplot(111)

    bins = np.arange(np.ceil(data.min()), np.floor(data.max()))
    print "cdf and pdf calculating: bins = %d" % len(bins)
    counts_cdf, base_cdf = np.histogram(data, bins=bins, normed=True)
    counts_pdf, base_pdf = np.histogram(data, bins=bins, normed=False)
    cdf = np.cumsum(counts_cdf)

    print counts_cdf
    print cdf
    print base_cdf

    print "start plotting!"

    cd = ax.plot(base_cdf[1:], [x*100 for x in cdf], 'b-', linewidth=1, label='Cumulative Distribution') #8
    ax2 = ax.twinx()
    nd = ax2.plot(base_cdf[1:], counts_pdf, 'r-', linewidth=1, label='Frequency Distribution')
    print "start labeling!"

    ax.set_xlim(xmin=1, xmax=xlim)
    ax.set_ylim(0, 1*100)
    ax2.set_ylim(0, max(counts_pdf))
    ax.set_xlabel(xlabel, fontsize=24)
    ax.set_ylabel('Cumulative % of'+y_type, fontsize=24)
    ax2.set_ylabel('Number of'+y_type, fontsize=24)

    ax.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax2.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    ax.get_yaxis().set_tick_params(labelsize = 24)
    ax2.get_yaxis().set_tick_params(labelsize = 24)
    ax.get_xaxis().set_tick_params(labelsize = 24)

    plt.legend(cd+nd, [l.get_label() for l in (cd+nd)], loc='center right', prop={'size':24})

    plt.grid()
    name = '%s.png' % xlabel.replace(" ", "_").replace("/","divided_by").replace(":","")
    fig.savefig(name)


""""""
def calculate_cdf(data1, ticks):
    data0 = np.array(data1)
    data = data0[data0 != np.array(None)]
    #data = np.array(data)
    print("plot: min = %d" % data.min())
    print("plot: max = %d" % data.max())
    print("plot: median = %d" % np.median(data))

    # ax = fig.add_subplot(111)

    bins = ticks #np.arange(np.ceil(data.min()), np.floor(data.max()))
    print "cdf and pdf calculating: bins = %d" % len(bins)
    counts_cdf, base_cdf = np.histogram(data, bins=bins, normed=True)
    counts_pdf, base_pdf = np.histogram(data, bins=bins, normed=False)
    cdf = np.cumsum(counts_cdf)

    print counts_cdf
    print counts_pdf
    print cdf
    print base_cdf

    print "start saving to files!"

    write_to_file('counts_cdf', counts_cdf, 'calculate')
    write_to_file('counts_pdf', counts_pdf, 'calculate')
    write_to_file('cdf', cdf, 'calculate')
    write_to_file('base_cdf', base_cdf, 'calculate')


def write_to_file(type, line, t_class):

    with open('%s_metrics_datas_%s.lst' % (t_class, type), 'a+') as f:
        json.dump(line, f)
        f.write(os.linesep)


def plot_bar_pic(fig, x, y, xlabel, ylabel, xlim, ticks):

    ax = fig.add_subplot(111)

    ax.set_xlim(xlim / ticks, xlim)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)

    xmajorLocator = MultipleLocator(xlim / ticks) 
    ax.xaxis.set_major_locator(xmajorLocator)

    width = 0.5 

    ax.bar(x, y, width=width)
    ax.grid()
    name = 'bar_%s%s.png' % (xlabel, ylabel)

    # bar_label_text(ax, x, y, xlim)

    fig.savefig(name)

