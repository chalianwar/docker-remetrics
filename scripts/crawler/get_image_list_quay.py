
import requests
import re
import os, sys, subprocess, select, random, urllib2, time, json, tempfile, shutil
import threading
import Queue

lock=threading.Lock()
fout=open('images.xls', 'w+')

sstr_docker_hub='https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=%d&pullCount=0&q=%s&starCount=0'
#print sstr_docker_hub
sstr_quay='https://quay.io/search?q=%s&page=%d'
#print sstr_quay
sstr_jfrog_artifactory=''
sstr_google_container=''

#each registry has its own queue

def get_list_from__quay():



def parse_webcode_for_dockerhub(sstr)
	sstr0=re.split('ssoEnabled', sstr)
	#print sstr0[len(sstr0)-1]
	sstr1=sstr0[len(sstr0)-1]

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

def queue_requests()

def get_list_from_dockerhub(word):
	for i in range(1, 6000): #6000
	        #sstr0="https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=%d&pullCount=0&q=%s&starCount=0" % (i, word)
	        f=requests.get(sstr0)
	        print "===========>>>>>====================>>>>"+f.url
	
	        sstr=f.content
	        pat='ssoEnabled'
		#sstr0=re.split('ssoEnabled', sstr)
		##print sstr0[len(sstr0)-1]
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

words=['a', 'ubuntu', 'docker', 'repo', 'node', 'red']

def main():
	print sstr_docker_hub
	print sstr_quay

	#for word in words:
	#	print word
	#	threading.Thread(target=process_url_word, args=(word,)).start()

if __name__=='__main__':
	main()
	exit(0)


