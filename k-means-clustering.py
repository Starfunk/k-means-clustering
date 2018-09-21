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

#How many centroids? Let's say 7 since matplotlib has 7 base colours.
N = int(input("Please enter the number of centroids you would like to use (1-7): "))
if N <= 0 or N >= 8:
	raise ValueError('Please enter a number bewteen 1 and 7.')

#The initial range of random numbers that a and b can take on.
centroids = []
for i in range(N):
	a = round(random.uniform(0,df.mean()[0]),1)
	b = round(random.uniform(0, df.mean()[1]),1)
	centroid = [a,b]
	centroids.append(centroid)

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
#Using an array for each point and updating the 3rd position with the label works.
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
	
def get_labels(points = []):
	labels = []
	for i in points:
		labels.append(i[2])
	return labels
	
#Label points and put them into an array.
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
		for k in points:
			if k[2] == j + 1:
				x_avg += k[0]
				y_avg += k[1]
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

#Plotting the clustered points!
x = df.iloc[:,0]
y = df.iloc[:,1]
label = get_labels(points)
colors = ['red','green','blue','purple','cyan','magenta','yellow','pink']
plt.scatter(x, y, c=label, cmap=matplotlib.colors.ListedColormap(colors))

#Plotting the centroids
color = ['black']
for i in centroids:
	plt.scatter(i[0], i[1], color=color)
	
plt.show()


