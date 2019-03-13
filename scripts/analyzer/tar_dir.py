
import os, tarfile, multiprocessing

dirname = "layer_db_json"
file_list = []
#tar_dir = ""

def load_dir(dirname):
	for path, _, filenames in os.walk(dirname):
		for filename in filenames:
        		print filename
            		absfilename = os.path.join(path, filename)
			print absfilename
            		file_list.append(absfilename)
            		#logging.debug('layer_tarball: %s, size %d', tarball_filename, f_size)


def chunks(l, n):
	return [l[i:i+n] for i in range(0, len(l), n)]


def process_file_list(f_list):
	abs_zip_file_name = f_list[0]+'tar.gz'

	tar = tarfile.open(abs_zip_file_name, "w:gz")
	for i in f_list:
		tar.add(i)
		print i
	tar.close()
	print "write to %s"%abs_zip_file_name


def main():
	load_dir(dirname)
	slices = chunks(file_list, 10000)
 	print len(slices)
        print "create pool"
        P = multiprocessing.Pool(60)
        print "before map!"
        P.map(process_file_list, slices)
        print "after map"

if __name__ == '__main__':
        print 'start!'
        main()
        print 'finished!'
