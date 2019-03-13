
import os, sys, subprocess, select, random, urllib2, time, json, tempfile, shutil
import re
import threading, Queue
import argparse
from optparse import OptionParser

q=Queue.Queue()
num_worker_threads=50

def pull(image):
	cmd='docker pull %s' % image
        try:
		rc = os.system(cmd)
	except:
		print e
                print 'Ooops: something wrong with this image: %s!' % name
                pass

def operation():
	while True:
		name=q.get()
        	if name is None:
			break
		pull(name)
		q.task_done()
       
def get_image_names(name):
	cmd1='cp %s image-list.xls' % name
	cmd2='awk -F\''+','+'\' \'{print $3}\' image-list.xls > image-names.xls'
	print cmd1
	print cmd2
	rc=os.system(cmd1)
	assert(rc == 0)
	rc=os.system(cmd2)
	assert(rc == 0)

def queue_names():
	with open('image-names.xls') as fd:
		for name in fd:
			if name: 
	        		print name
				q.put(name)

threads=[]
def main():
	parser = OptionParser()
	parser.add_option('-f', '--filename', action='store', dest='filename', help="The input file which contains all the images'names", default="images.tsv")
	options, args = parser.parse_args()
	print 'Input file name: ', options.filename

	get_image_names(options.filename)
	queue_names()
	start = time.time()
	for i in range(num_worker_threads): 
		t=threading.Thread(target=operation)
		t.start()
		threads.append(t)

	q.join()
	print 'wait here!'
	for i in range(num_worker_threads):
		q.put(None)
	print 'put here!'
	for t in threads:
		t.join()
	print 'done here!'

	elapsed = time.time() - start
        print (elapsed / 3600)


if __name__=='__main__':
	main()
	print 'should exit here!'
	exit(0)


