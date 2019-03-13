

import re, os
total_size=0
tmp=0
fp=open('ls_size_out.xls', 'w+')

cmd1='docker image ls > image_ls.xls'
#cmd1='awk -F\' \' '{print $7}' image_ls.xls > ls_size.xls
cmd2='awk -F\''+' '+'\' \'{print $7}\' image_ls.xls > ls_size.xls'
cmd3='wc -l ls_size.xls'
print cmd1
print cmd2
print cmd3
rc=os.system(cmd1)
assert(rc == 0)
rc=os.system(cmd2)
assert(rc == 0)
#rc=os.system(cmd3)
#assert(rc == 0)


with open('ls_size.xls') as fd:
        #for line in fd:
                #line=fd.readlines()
                for size in fd: #line:
                        #print size
			unit=re.findall("[a-zA-Z]+", size)
			print unit
			num=re.split("[a-zA-Z]+", size)
			print num
			if len(unit) > 0:
				print unit
				if unit[0]:
					if unit[0] == 'GB':
						tmp=float(num[0])*1024  
						print tmp
						fp.writelines(str(tmp)+'\tMB\n')
					elif unit[0] == 'MB':
						tmp=float(num[0])
						print tmp
						fp.writelines(str(tmp)+'\tMB\n')
					total_size=total_size+tmp


#total_size=total_size/1024
print 'total_size:%d MB; %d GB' % (total_size, total_size/1024)
rc=os.system(cmd3)
assert(rc == 0)


