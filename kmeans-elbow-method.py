import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import math 

#Import the dataset
df = pd.read_csv("kmeans.csv")

#Recording # of rows of the data set
rows = df.shape[0]

#Recording # of rows of the data set
cols = df.shape[1]

#Records all the points in the graph
points = []

#Number of centroid updating rounds
N = 25

#Record the scores for each value of k:
scores = []

#Number of k we test for 
k = 6

#Now label every point based on the point it is closed to.
def distance(x,y,centroid = []):
	#x and y coordinates of the centroid
	a = centroid[0]
	b = centroid[1]
	#Applying the pythagorean theorem. Where k is the distance bewteen
	#the centroid and the point in question.
	i = abs(b-y)
	j = abs(a-x)
	k = math.sqrt(i ** 2 + j ** 2)
	return k
	
#The label on each point corresponds with the index of the centroids.
#Using an array for each point and updating the 3rd position with the label would work.
def label_point(x,y,centroids = []):
	minimum_distance = 100000
	label = 1
	counter = 1
	for i in centroids:
		d = distance(x,y,i)
		if d < minimum_distance:
			label = counter
			minimum_distance = d
		counter += 1 
	return label 


#The label on each point corresponds with the index of the centroids.
#Using an array for each point and updating the 3rd position with the label works.
def get_labels(points = []):
	labels = []
	for i in points:
		labels.append(i[2])
	return labels

#Start of program
print("Computing the k-Means Elbow Graph from k = 1 to k = " + str(k) + ".")

for k_round in range(k):
	centroids = []
	for i in range(N):
		a = round(random.uniform(0,df.mean()[0]),1)
		b = round(random.uniform(0, df.mean()[1]),1)
		centroid = [a,b]
		centroids.append(centroid)

	#Label points and put them into array.
	for i in range(rows):
		point = df.iloc[i,:]
		x = point[0]
		y = point[1]
		label = label_point(x,y,centroids)
		point = [x,y,label]
		points.append(point)

	#Update centroids N times.	
	for i in range(N):
		for j in range(len(centroids)):
			centroid = centroids[j]
			x_avg = 0
			y_avg = 0
			count = 0
			for t in points:
				if t[2] == j + 1:
					x_avg += t[0]
					y_avg += t[1]
					count += 1
			if count == 0:
				count = 2
			x_avg = x_avg / count
			y_avg = y_avg / count
			centroids[j][0] = x_avg
			centroids[j][1] = y_avg
		
		for i in range(len(points)):
			point = points[i]
			x = point[0]
			y = point[1]
			label = label_point(x,y,centroids)
			points[i][2] = label
			
	#Calculating how good the clustering was.	
	for point in points:
		score = 0
		x = point[0]
		y = point[1]
		centroid = centroids[point[2]-1]
		d = distance(x,y,centroid)
		score += d ** 2
	score = score/(k_round+1)
	print("The " + str(k_round + 1) + "th round has been computed.")
	score_array = [(k_round+1),score]
	scores.append(score_array)

for i in range(len(scores)):
	plt.scatter(scores[i][0],scores[i][1],c='black')
plt.xlabel('k-value', fontsize=10)
plt.ylabel('Sum of distances to centroid squared over k-value', fontsize=10)
plt.show()
