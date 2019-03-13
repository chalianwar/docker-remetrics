
import requests
import re
import os, sys, subprocess, select, random, urllib2, time, json, tempfile, shutil
import threading
import Queue

#lock=threading.Lock()
#fout=open('images-quay.xls', 'w+')

def process_url_word(word):
	for i in range(1, 2):
	        sstr0="https://quay.io/search?q=%s&page=%d" % (word, i)
	        f=requests.get(sstr0)
	        print "===========>>>>>====================>>>>"+f.url
	
	        sstr=f.content
		print '%s' % sstr
	        #pat='ssoEnabled'
		#sstr0=re.split('ssoEnabled', sstr)
		#print sstr0[len(sstr0)-1]
        	#sstr1=sstr0[len(sstr0)-1]
		#
	        #if sstr1:
	        #	sstr=re.split('\[\]', sstr1)
		#	if len(sstr)>2:
		#		sstr2=sstr[2]
		#	if sstr2: 
	        #		sstr=re.split('":\[{', sstr2)
		#		if len(sstr)>1:
		#			sstr3=sstr[1]
		#			if sstr3:
	        #				sstr4=re.split('}\]',sstr3)[0]
		#				if sstr4:
	        #					sstr5=re.split('},{', sstr4)
		#					lock.acquire()     
	        #					for i in sstr5:
	        #					        parts=re.split(',"', i)
	        #					        print parts
	        #					        for j in parts:
	        #					                if j:
	        #					                        print j
	        #					                        args=re.split('":', j)[1].replace('"','').replace('\u002F', '/')
	        #					                        print args
	        #					                        fout.writelines(args+'\t')
	        #					        fout.writelines('\n')
		#					lock.release()

#words=['a', 'ubuntu', 'docker', 'repo', 'node', 'red']
words=['docker']
def main():
	for word in words:
		print word
		threading.Thread(target=process_url_word, args=(word,)).start()

if __name__=='__main__':
	main()
	exit(0)


