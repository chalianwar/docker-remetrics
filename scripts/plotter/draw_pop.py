
from draw_pic import *


def main():
        parser = optparse.OptionParser()
        parser.add_option('-f', '--filename', action='store', dest="filename", help="The input file name. e.g., images.tsv", default="images.tsv")
        options, args = parser.parse_args()

        print ('Input file name: %s', options.filename)

	image_pop_filename = options.filename

	cmd_stars='awk -F\''+r','+'\' \'{print $1}\' %s > image_stars.txt' % image_pop_filename
	cmd_pulls='awk -F\''+r','+'\' \'{print $2}\' %s > image_pulls.txt' % image_pop_filename
	print cmd_stars
	print cmd_pulls

	os.system(cmd_stars)
	os.system(cmd_pulls)
	
	columns_stars=np.loadtxt('image_stars.txt')
	columns_pulls=np.loadtxt('image_pulls.txt')
	
	print columns_stars
	print columns_pulls
	
	data_stars=columns_stars
	data_pulls=columns_pulls

	fig = fig_size('min')  # 'large'

	data = data_stars
	xlabel = 'Star count for each image'  # data = [x * 1.0 / 1024 / 1024 for x in data1]
	xlim = 5  # max(data1)
	ticks = 25
	print xlim
	plot_cdf(fig, data, xlabel, xlim, ticks, "stars")
	
	fig = fig_size('min')  # 'large'
	
	data = data_pulls
	xlabel = 'Pull count for each image'  # data = [x * 1.0 / 1024 / 1024 for x in data1]
	xlim = 250  # max(data1)
	ticks = 25
	print xlim
	plot_cdf(fig, data, xlabel, xlim, ticks, "pull count")

if __name__=='__main__':
	print 'here'
	main()
	print 'finished!'
	exit(0)

