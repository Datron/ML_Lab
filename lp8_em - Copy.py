import csv
import math
import copy
k=4

class cluster:
	def __init__(self,cluster_head_data):
		self.head=cluster_head_data
		self.l=[]
		self.mean=cluster_head_data[0]
		self.variance=1.0
	
	def display_head(self):
		print("m=",self.mean)
		print("v=",self.variance)
	
	def add_ele_cluster(self,data):
		self.l.append(data)
		print(self.l)
	
	def display_ele(self):
		print('list contains',self.l)
		
def find_insert_individual_cluster(cluster,element,n):
	ele=float(element[0])
	prob=[]
	for i in range(len(cluster)):
		pxb=1/math.sqrt(2*3.142*cluster[i].variance)*math.exp(-1*(ele-float(cluster[i].mean))**2/(2*float(cluster[i].variance)))
		print('pxb exact==',pxb)
		prob.append(pxb)
	print('prob elem',prob)
	bi_den=0
	for i in range(len(prob)):
		bi_den = bi_den+prob[i]*1/n
		print('bi den',bi_den)
	for i in range(len(cluster)):
		clust_data=[]
		clust_data.append(ele)
		bi=(prob[i]*1/n)/bi_den
		clust_data.append(bi)
		cluster[i].add_ele_cluster(clust_data)
			
def recalculate_cluster_mean_variance(cluster):
	l1=cluster.l
	print('list entries',l1)
	mean_num=0.0
	mean_den=0.0
	var_num=0.0
	var_den=0.0
	for i in range(len(l1)):
		mean_num=mean_num+l1[i][0]*l1[i][1]
		mean_den=mean_den+l1[i][1]
	mean=mean_num/mean_den
	cluster.mean=mean
	for i in range(len(l1)):
		var_num=var_num+l1[i][1]*(l1[i][0]-mean)**2
		var_den=var_den+l1[i][1]
	variance=var_num/var_den
	cluster.variance=mean
	
def find_nearest(cluster,ele):
	ele=float(ele[0])
	nearest_prob=None
	index=1
	for i in range(len(cluster)):
		pxb=1/math.sqrt(2*3.142*cluster[i].variance)*math.exp(-1*(ele-float(cluster[i].mean))**2/(2*float(cluster[i].variance)))
		print('pxb for cluster i',i,'=',pxb)
		if nearest_prob is None:
			nearest_prob=pxb
			index=i
		else:
			if nearest_prob<pxb:
				nearest_prob=pxb
				index=i
	print('index',index,'nearest_prob=',nearest_prob)
	cluster[index].l.append(ele)
	
with open('cluster.csv') as csvfile:
	spamreader = csv.reader(csvfile,delimiter=',')
	db=[]
	for row in spamreader:
		db.append(row)
print('Db Enteries')
print(db)
c=[]

for i in range(k):
	new_clust=cluster(db[i])
	c.append(new_clust)
print('initial cluster Mean Variance')

for i in range(k):
	print('-----cluster=',i,'-----')
	c[i].display_head()
	
error_ratio=1

while error_ratio>0:
	error_ratio=0
	prev=copy.deepcopy(c)
	for i in range(len(db)):
		find_insert_individual_cluster(c,db[i],len(db))
	for i in range(len(c)):
		recalculate_cluster_mean_variance(c[i])
	for i in range(k):
		print('-----cluster',i,'-----')
		c[i].display_head()
		for i in range(k):
			c[i].l=[]
		error_ratio=0
		for i in range(len(c)):
			if abs(c[i].variance-prev[i].variance)>0.1:
				error_ratio=error_ratio+1

for i in range(k):
	c[i].l=[]
	
for i in range(len(db)):
	find_nearest(c,db[i])

for i in range(len(c)):
	print(c[i].l)		                                  
