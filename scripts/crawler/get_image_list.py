
import argparse
from optparse import OptionParser
import requests
import re
import os, sys, subprocess, select, random, urllib2, time, json, tempfile, shutil
import threading
import Queue

#filename=sys.argv[1]
#fout=open(filename, 'w+')
#num_pages=600000
#fout = None
words=['*']
sstr_docker_non_official='https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=%d&pullCount=0&q=%s&starCount=0'
sstr_docker_official='https://hub.docker.com/explore/?page=%d'

lock=threading.Lock()

def process_url_word(fout, word, is_nonofficial):
	#for i in range(1, num_pages):
	page_no = 0
	while True:
		page_no = page_no + 1
		if is_nonofficial:
	        #sstr0="https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=%d&pullCount=0&q=%s&starCount=0" % (page_no, word)
	        	sstr0 = sstr_docker_non_official % (page_no, word)
		else:
			sstr0 = sstr_docker_official % page_no
		f=requests.get(sstr0)
		if f.status_code == requests.codes.ok:
	        	print "===========>>>>>====================>>>>"+f.url
		#else:
		if f.status_code == 404:
			break
	        sstr=f.content
	        pat='ssoEnabled'
		sstr0=re.split('ssoEnabled', sstr)
		#print sstr0[len(sstr0)-1]
        	sstr1=sstr0[len(sstr0)-1]
		if not sstr1:
			break
		#sstr1=None	
	        if sstr1:
	        	sstr=re.split('\[\]', sstr1)
			if len(sstr)>2:
				sstr2=sstr[2]
			if sstr2: 
	        		sstr=re.split('":\[{', sstr2)
				if len(sstr)>1:
					sstr3=sstr[1]
					if sstr3:
	        				sstr4=re.split('}\]',sstr3)[0]
						if sstr4:
	        					sstr5=re.split('},{', sstr4)
							lock.acquire()     
	        					for i in sstr5:
	        					        parts=re.split(',"', i)
	        					        print parts
	        					        for j in parts:
	        					                if j:
	        					                        print j
	        					                        args=re.split('":', j)[1].replace('"','').replace('\u002F', '/')
	        					                        print args
	        					                        fout.writelines(args+'\t')
	        					        fout.writelines('\n')
							lock.release()
#words=['/']
#words=['a', 'ubuntu', 'docker', 'repo', 'node', 'red']

#parser=OptionParser()
#parser.add_option('-f', '--filename', action='store', dest="query")

def main():
	#parser = argparse.ArgumentParser(description='Get a list of images\'names from Docker Hub.')
	#parser.add_argument('-f', '--filename', action='store', dest="filename", help='The output file name. e.g., images.tsv', default="images.tsv")
	parser = OptionParser()
	parser.add_option('-f', '--filename', action='store', dest="filename", help="The output file name. e.g., images.tsv", default="images.tsv") 
	options, args = parser.parse_args()
	#print parser.filename
	print 'Output file name: ', options.filename
	#parser.add_argument('string', metavar='-f', action=GetOutPutName, type=str, nargs=1, help='The output file name. e.g., images.tsv')
	#args=parser.parse_args()
	#filename=sys.argv[1]       
	fout = open(options.filename, 'w+') 
	for word in words:
		print word
		threading.Thread(target=process_url_word, args=(fout, word, True,)).start()
		threading.Thread(target=process_url_word, args=(fout, word, False,)).start()


if __name__=='__main__':
	main()
	exit(0)


