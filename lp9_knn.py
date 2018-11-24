import csv
import random
import math
import operator

def load_dataset(filename, split, training_set=[],test_set=[]):
	with open(filename) as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for x in range(len(dataset)-1):
			for y in range(4):
				dataset[x][y] = float(dataset[x][y])
			if random.random() < split:
				training_set.append(dataset[x])
			else:
				test_set.append(dataset[x])

def euclidean_distance(instance1,instance2,length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]),2)
	return math.sqrt(distance)
	
def get_neighbors(training_set,test_instance,k):
	distances = []
	length = len(test_instance)-1
	for x in range(len(training_set)):
		dist = euclidean_distance(test_instance,training_set[x],length)
		distances.append((training_set[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def get_response(neighbors):
	class_votes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in class_votes:
			class_votes[response] += 1
		else:
			class_votes[response] = 1
	sorted_votes = sorted(class_votes.items(),key=operator.itemgetter(1),reverse=True)
	return sorted_votes[0][0]

def get_accuracy(test_set,predictions):
	correct = 0
	for x in range(len(test_set)):
		if test_set[x][-1] == predictions[x]:
			correct += 1
	return (correct/float((len(test_set))) * 100.0)

def main():
	# prepare data
	training_set = []
	test_set = []
	split = 0.67
	load_dataset('KNN-input.csv',split,training_set,test_set)
	print('\n Number of training data:'+ (repr(len(training_set))))
	print('\n Number of test data:' + (repr(len(test_set))))
	# generate predictions
	predictions = []
	k = 3
	print("\n the predictions are:")
	for x in range(len(test_set)):
		neighbors = get_neighbors(training_set,test_set[x],k)
		result = get_response(neighbors)
		predictions.append(result)
		print('predicted ='+repr(result)+', actual='+repr(test_set[x][-1]))
	accuracy = get_accuracy(test_set,predictions)
	print('\n The accuracy is:'+repr(accuracy) + '%')


main()
