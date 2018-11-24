import csv
import math
import copy

k=2

class cluster:
	def __init__(self,cluster_head_data):
		self.head = cluster_head_data
		self.l = []
	
	def display_head(self):
		print(self.head)
	
	def add_ele_cluster(self,data):
		self.l.append(data)
		
	def display_ele(self):
		print('list contains',self.l)
	
def compare_the_values(first,second):
	x = float(first[0])
	x1 = float(second[0])
	val = math.sqrt(math.pow(math.fabs(x-x1),2)+math.pow(math.fabs(x-x1),2))
	return val

def compare_the_nearest_cluster(cluster,data):
	# initialize the nearest cluster to 0
	dist_measure = None
	nearest = 0
	for i in range(len(cluster)):
		dist = compare_the_values(cluster[i].head,data)
		if dist_measure is None:
			dist_measure = dist
			nearest = i
		if dist < dist_measure:
			dist_measure = dist
			nearest = i
	return nearest

def recal_head(cluster):
	for i in range(len(cluster)):
		l1 = cluster[i].l
		xval = 0.0
		yval = 0.0
		for j in l1:
			xval += float(j[0])
			yval += float(j[1])
		xavg = xval/len(l1)
		yavg = yval/len(l1)
		avg1 = []
		avg1.append(xavg)
		avg1.append(yavg)
		cluster[i].head = avg1
# read the contents of the csv file
with open("cluster.csv") as csvfile:
	spamreader = csv.reader(csvfile,delimiter=",")
	#insert elements into the list
	db = []
	for row in spamreader:
		db.append(row)
	# creating individual cluster heads
#display elements of the list
print("DB entries")
print(db)

#init cluster
c = []
for i in range(k):
	new_clust = cluster(db[i])
	c.append(new_clust)
print("Initial cluster head values")
for i in range(k):
	print("-------cluster",i,"-------")
	c[i].display_head()
error_rate = 1
# iteration and including element in cluster
while error_rate > 0:
	prevc = copy.deepcopy(c)
	for ele in db:
		r = compare_the_nearest_cluster(c,ele)
		c[r].add_ele_cluster(ele)
	#display all elements
	for clust in c:
		clust.display_ele()
	#recalculate head
	recal_head(c)
	for i in range(k):
		print("--------cluster",i,"-----------")
		c[i].display_head()
	# remove the ele of cluster head for next iteration
	for i in range(k):
		c[i].l = []
	# calculate error
	error_rate = 0
	for i in range(k):
		if c[i].head != prevc[i].head:
			error_rate += 1
#final cluster ele
