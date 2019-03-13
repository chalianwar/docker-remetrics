
import sys
sys.path.append('../libraries/')
sys.path.append('../analyzer/')
from graph_related_libraries import *
from config import *

image_growth_filename1 = 'images-5-30-7-11-cnt.txt'
image_growth_filename2 = "images-7-26-9-20-cnt.txt"

data0 = np.loadtxt(image_growth_filename2)

images_cnt = [data0[i] for i in range(0, len(data0), 24)]

print images_cnt

print len(images_cnt)

data0 = np.trim_zeros(images_cnt)

print data0

print len(data0)

x = np.arange(0, len(data0), 1)

base1 = datetime.datetime(2017, 5, 30)
base2 = datetime.datetime(2017, 7, 26)
arr = np.array([base2 + datetime.timedelta(days=i) for i in xrange(len(data0))])

print arr

plt.rcParams.update({'font.size': 20})
fig = plt.figure(figsize=(12, 8), dpi=80)

ax = fig.add_subplot(111)

plt.xlabel('Time (Days)')
plt.ylabel('Number of repositories in Docker hub')

#ax.xaxis.set_major_locator(DayLocator(interval=6))
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d'))

#ax.xaxis.set_major_locator(WeekdayLocator(byweekday=MO, interval=4))
#ax.set_xlim([datetime.date(2017, 5, 30), datetime.date(2017, 7, 11)])

#xmajorLocator = MultipleLocator(1)
#ax.xaxis.set_major_locator(xmajorLocator)
# plt.xlim(0, 200000)
line = plt.plot(arr, data0, 'b-')
plt.setp(line, color='r', linewidth=1.0)
#plt.xticks(np.arange(datetime.date(2017, 5, 30), datetime.date(2017, 7, 11), datetime.timedelta(days=3)))
# ax=fig.add_subplot(212)
#
# plt.xlabel('200K images (Name)')
# plt.ylabel('Pull count')
# #plt.title(pull count)
# xmajorLocator=MultipleLocator(10000)
# ax.xaxis.set_major_locator(xmajorLocator)
#plt.xlim(datetime.date(2017, 5, 30), datetime.date(2017, 7, 11), auto=True)
# plt.plot(x, data_pulls, 'r')
plt.grid()
plt.savefig('growth_%s.png'%image_growth_filename2.replace(".txt",""))
