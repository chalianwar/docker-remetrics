import os, subprocess, multiprocessing
mv_dir = "configs"
layers = []

#with open("layers.json.lst") as f:
#       for line in f:
#               layers.append(line)

def process_line(line):
        filename = os.path.join("layers", line.replace("\n", ""))
	cmd2 = 'file %s' % filename
	proc = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
    	out, err = proc.communicate()
    	print out

    	if 'text' not in out:
        	return
    	#else:
	#	return True

        cmd="mv %s"%(filename+' '+mv_dir)
        print cmd
        try:
                subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
        except subprocess.CalledProcessError as e:
                print '###################%s: exit code: %s; %s###################'% (cmd, e.returncode, e.output)


def main():
        with open("configs.file.lst") as f:
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
