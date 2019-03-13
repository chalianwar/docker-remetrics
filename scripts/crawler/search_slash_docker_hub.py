
import argparse
from optparse import OptionParser
import requests
import re
import os, sys, subprocess, select, random, urllib2, time, json, tempfile, shutil
import threading
import Queue
from datetime import datetime
import sched, time
#from apscheduler.schedulers.blocking import BlockingScheduler
#from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.triggers.interval import IntervalTrigger
#filename=sys.argv[1]
#fout=open(filename, 'w+')
#num_pages=600000
#fout = None
words=['/']
sstr_docker_non_official='https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=%d&pullCount=0&q=%s&starCount=0'
sstr_docker_official='https://hub.docker.com/explore/?page=%d'

#lock=threading.Lock()

def print_word_count(fout, word):
	#for i in range(1, num_pages):
	#page_no = 0
	#while True:
	#	page_no = page_no + 1
	#	if is_nonofficial:
	        #sstr0="https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=%d&pullCount=0&q=%s&starCount=0" % (page_no, word)
	        sstr0 = sstr_docker_non_official % (1, word)
	#	else:
	#		sstr0 = sstr_docker_official % page_no
		f=requests.get(sstr0)
		#if f.status_code == requests.codes.ok:
	        #	print "===========>>>>>====================>>>>"+f.url
		#else:
		#if f.status_code == 404:
		#	break
	        sstr=f.content
	        pat='Repositories'
		sstr0=re.split('Repositories', sstr)
		#print sstr0[len(sstr0)-1]
        	sstr1=sstr0[len(sstr0)-1]
		print len(sstr0)
		#print sstr1
		#fd = open('tmp.txt', 'w+')
		#fd.write(sstr1)
		#fd.close()
		#sstr1=None	
	        if sstr1:
	        	sstr=re.split('<', sstr1)
			#fd.write(sstr)
			#print sstr[0]
			#fd.close()
			if len(sstr)>2:
				sstr2=sstr[0].replace('(', '').replace(')', '').replace(' ', '')
				print sstr2
				fout.writelines(sstr2+'\n')
				fout.flush()
			#if sstr2: 
	        		#sstr=re.split('":\[{', sstr2)
				#if len(sstr)>1:
				#	sstr3=sstr[1]
				#	if sstr3:
	        		#		sstr4=re.split('}\]',sstr3)[0]
				#		if sstr4:
	        		#			sstr5=re.split('},{', sstr4)
				#			lock.acquire()     
	        		#			for i in sstr5:
	        		#			        parts=re.split(',"', i)
	        		#			        print parts
	        		#			        for j in parts:
	        		#			                if j:
	        		#			                        print j
	        		#			                        args=re.split('":', j)[1].replace('"','').replace('\u002F', '/')
	        		#			                        print args
	        		#			                        fout.writelines(args+'\t')
	        		#			        fout.writelines('\n')
				#			lock.release()
#words=['/']
#words=['a', 'ubuntu', 'docker', 'repo', 'node', 'red']

#parser=OptionParser()
#parser.add_option('-f', '--filename', action='store', dest="query")

def search_job(s, fout):
	print "Time: %s. start search...." % str(datetime.now())
	fout.writelines(str(datetime.now())+'\t')
	for word in words:                                                            	
        	print word
		fout.writelines(word+'\t')
        	threading.Thread(target=print_word_count, args=(fout, word,)).start()
	s.enter(3600, 1, search_job, (s,fout,))

def main():
	#parser = argparse.ArgumentParser(description='Get a list of images\'names from Docker Hub.')
	#parser.add_argument('-f', '--filename', action='store', dest="filename", help='The output file name. e.g., images.tsv', default="images.tsv")
	parser = OptionParser()
	parser.add_option('-f', '--filename', action='store', dest="filename", help="The output file name. e.g., search_images_count.tsv", default="search_images_count.tsv") 
	options, args = parser.parse_args()
	#print parser.filename
	print 'Output file name: ', options.filename
	#parser.add_argument('string', metavar='-f', action=GetOutPutName, type=str, nargs=1, help='The output file name. e.g., images.tsv')
	#args=parser.parse_args()
	#filename=sys.argv[1]       
	fout = open(options.filename, 'w+') 
	
	s = sched.scheduler(time.time, time.sleep)
	s.enter(3600, 1, search_job, (s,fout,))
	s.run()
	#scheduler = BlockingScheduler()
	#scheduler.add_job(search_job, 'interval', hours=1)
	#scheduler.start()
	#for word in words:
	#	print word
	#	threading.Thread(target=print_word_count, args=(fout, word,)).start()

		#threading.Thread(target=process_url_word, args=(fout, word, False,)).start()


if __name__=='__main__':
	main()
	exit(0)


