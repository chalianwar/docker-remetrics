import os, sys
import numpy as np
from optparse import OptionParser

class ImagesBase:

	def __init__(self, filename):
		print "load file: %s" % filename
		datatype = np.dtype({
		'names':('star_count', 'pull_count', 'name'),
		'formats':('i', 'i', 'S128')
		})
		self.raw_data = np.loadtxt(filename, delimiter=',', dtype = datatype)
		print self.raw_data
	def sortby(self, field):
		if field == 'pull_count':
			self.sorted_data = np.sort(self.raw_data, order = 'pull_count')
			print self.sorted_data
		elif field == 'star_count':
			self.sorted_data = np.sort(self.raw_data, order = 'star_count')
			print self.sorted_data
		elif field == 'all_two':
			self.sorted_data = np.sort(self.raw_data, order = ['pull_count', 'star_count'])
			print self.sorted_data
		return self.sorted_data

def main():
        parser = OptionParser()
        parser.add_option('-f', '--filename', action='store', dest='filename', help="The input file which contains all the images'names", default="images.tsv")
        options, args = parser.parse_args()
        print 'Input file name: ', options.filename
	
	cmd1='awk -F\''+r'\t'+'\' \'{print $1 "," $2 "," $7}\' %s > tmp.txt' % options.filename
	rc=os.system(cmd1)
        assert(rc == 0)

	imagesbase = ImagesBase('tmp.txt')

	field = 'pull_count'
	data = imagesbase.sortby(field)
	np.savetxt('pull_count_sorted.out', data, fmt = "%d, %d, %s")
	field = 'star_count'        
	data = imagesbase.sortby(field)
        np.savetxt('star_count_sorted.out', data, fmt = "%d, %d, %s")
	field = 'all_two'
        data = imagesbase.sortby(field)
        np.savetxt('all_two_sorted.out', data, fmt = "%d, %d, %s")
	

if __name__=='__main__':
        print 'here'
        main()
        print 'finished!'
        exit(0)
