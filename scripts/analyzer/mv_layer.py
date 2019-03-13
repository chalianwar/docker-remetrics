
import os, subprocess, multiprocessing
mv_dir = "layer_db_json_bison02"
layers = []

#with open("layers.json.lst") as f:
#	for line in f:
#		layers.append(line)

def process_line(line):
	filename = os.path.join("layer_db_json", line.replace("\n", ""))
	cmd="mv %s"%(filename+' '+mv_dir)
	print cmd
	try:
		subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
	except subprocess.CalledProcessError as e:
        	print '###################%s: exit code: %s; %s###################'% (cmd, e.returncode, e.output)


def main():
	with open("layers.json.lst") as f:
        	for line in f:
                	layers.append(line)
    	print "create pool"
    	P = multiprocessing.Pool(60)
    	print "before map!"
	P.map(process_line, layers)
	print "after map"

if __name__ == '__main__':
        print 'start!'
        main()
        print 'finished!'
