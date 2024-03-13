#Devin Zhao, PA1
import math
import random
import datetime
import time

class Point:
    #The Point class is used to store the data of a point - its x and y coordinates
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
    #I implemented the __str__ function to customize its representation to a Cartesian form
    def __str__(self):
        return f"({self.x},{self.y})"

class Euclid_Pair:
    #The Euclid_Pair class is used to store the data of a connection between two points and the length of the connection
    def __init__(self, point1, point2, distance):
        self.point_a = point1
        self.point_b = point2
        self.dist = distance
    #__str__ was implemented to customize its formatting to look nice when outputted
    def __str__(self):
        return f"{self.point_a} {self.point_b} distance: {self.dist}"
    #getdist() was implemented for easier access to the dist class variable
    def getdist(self):
        return self.dist

def euclidian_dist(point_a, point_b):
    #euclidian_dist takes two points and calculates the distance between them using the Pythagorean Theorem
    #input: Points point_a, point_b
    #output: distance as a float
    return math.sqrt(pow(point_a.x - point_b.x,2) + pow(point_a.y-point_b.y,2))

def find_all_dist(data_points):
    #find_all_dist finds all possible distances between every point in a Point list
    #input: Point []
    #output: Euclid_Pair []
    dist_results = []
    for index_1 in range(0,(len(data_points)-1)):
        for index_2 in range(index_1+1,len(data_points)):
            #the nested for loop was used to prevent any duplicate comparisons from being made
            pair_points = Euclid_Pair(data_points[index_1], data_points[index_2], euclidian_dist(data_points[index_1],data_points[index_2]))
            #a Euclid_Pair object is made and is appended to the output list
            dist_results.append(pair_points)
    return dist_results

def euclid_pair_merge(ep_array, start, middle, end):
    #euclid_pair_merge is a revised version of the merge algorithm to account for the Euclid_Pair object
    left_end = middle - start + 1
    right_end = end - middle
    left_merge_array = []
    right_merge_array = []
    #the input array is split into two separate arrays and the subarrays are populated based on the middle partition
    for left_index in range(0,left_end):
        left_merge_array.append(ep_array[start + left_index])
    for right_index in range(0,right_end):
        right_merge_array.append(ep_array[middle + 1 + right_index])
    left_iterator = 0
    right_iterator = 0
    merge_index = start
    #I used a while loop to cycle through the subarrays, compare each other, and merge them back into the main array
    #also, manually setting the iterators makes implementing merging the leftover values easier
    while (left_iterator < left_end) and (right_iterator < right_end):
        left_dist = left_merge_array[left_iterator].getdist()
        right_dist = right_merge_array[right_iterator].getdist()
        if left_dist <= right_dist:
            ep_array[merge_index] = left_merge_array[left_iterator]
            left_iterator += 1
        else:
           ep_array[merge_index] = right_merge_array[right_iterator]
           right_iterator += 1
        merge_index += 1
    #this while loop merges any remaining values in the left-hand array back into the main array
    while left_iterator < left_end:
        ep_array[merge_index] = left_merge_array[left_iterator]
        merge_index += 1
        left_iterator += 1
    #this while loop merges any remaining values in the right-hand array back into the main array
    while right_iterator < right_end:
        ep_array[merge_index] = right_merge_array[right_iterator]
        merge_index += 1
        right_iterator += 1

def euclid_merge_sort(ep_array, start, end):
    #euclid_merge_sort is implemented as seen in the textbook
    if start < end:
        middle = (start + end-1)//2
        euclid_merge_sort(ep_array, start, middle)
        euclid_merge_sort(ep_array, middle + 1, end)
        euclid_pair_merge(ep_array, start, middle, end)

def find_shortest_distances(P,m):
    #find_shortest_distances is the main function - it finds all the possible distances, sorts them in descending order, and provides an output list
    #input: Point [] P, int m
    #output: Euclid_Pair[] shortest_distances of length m
    shortest_distances = []
    all_distances = find_all_dist(P)
    #this check is to make sure that if there is only 1 distance, then it doesn't need sorting
    #otherwise, it will cause the mergesort to error out
    if (len(all_distances) > 1):
        euclid_merge_sort(all_distances,0,len(all_distances)-1)
    #mth smallest results are appended to output array
    for index in range(0,m):
        shortest_distances.append(all_distances[index])
    return shortest_distances

#File I/O + timing
timestamp = datetime.datetime.today()
#I used the time of running to create custom output file names to prevent rewriting
output_file = open(f"PA1_{timestamp.year}_{timestamp.month}_{timestamp.day}_{timestamp.hour}_{timestamp.minute}_{timestamp.second}_output.txt","w")
points = []
results = []
incorrect_length = True
#I implemented the while loop to make sure that the user can give the most ideal input for n (number of points in list P)
while incorrect_length:
    #try-except block checks if the input is an integer
    try:
        points_length = int(input("Value of n (length of points list P): "))
    except ValueError:
        print("Input must be an integer. Please try again.")
    else:
        #the list length cannot be negative
        if points_length < 0:
            print("List length cannot be less than 0. Please try again.")
        #I let inputs of 0 and 1 pass because technically, you can have an empty list or a list of 1 value
        elif points_length == 0:
            print("No points will be generated.")
            incorrect_length = False
        #it just means that there would be no lengths to calculate
        elif points_length == 1:
            print("A point will be generated, but no length will be calculated.")
            incorrect_length = False
        else:
            incorrect_length = False
incorrect_input = True
#I implemented this while loop to make sure that the user has their ideal value of m (# of outputted results)
while incorrect_input:
    #try-except block checks if the input is an int
    try:
        iterations = int(input(f"Value of m? Input cannot be greater than {math.comb(points_length,2)}: "))
    except ValueError:
        print("Input must be an integer. Please try again.")
    else:
        #number of outputs must be greater than 0
        if iterations < 0:
            print("Input must be greater than 0. Please try again.")
        #number of outputs has a limit of nC2
        elif iterations > math.comb(points_length,2):
            print("Value too high. Please try again.")
        #technically, no outputs is valid - it just defeats the purpose of the algorithm
        elif iterations == 0:
            print("No distances will be printed in the output.")
            incorrect_input = False
        else:
            incorrect_input = False
output_file.write(f"m = {iterations}\n")
output_file.write(f"n = {points_length}\n\nPoints in P:\n")
#this for loop generates all the points - up to ~4 million unique points can be generated
for index in range(0,points_length):
    x_coord = random.randint(-1000,1000)
    y_coord = random.randint(-1000,1000)
    points.append(Point(x_coord, y_coord))
    output_file.write(f"{Point(x_coord,y_coord).__str__()}\n")
#I decided to start timing when the distance finding + sorting algorithm starts, as it makes the most sense
time_start = time.time()
results = find_shortest_distances(points,iterations)
time_end = time.time()
#results of the find_shortest_distances function are written in the output file
output_file.write("\nClosest Distances (formatted by coordinates of two points and their distance)\n")
for index in range(len(results)):
    output_file.write(f"{results[index].__str__()}\n")
#handy reminder of what the output file of the run is
print(f"Results can be found at {output_file.name}.")
output_file.write(f"\nTime taken: {time_end-time_start} seconds")
output_file.close()
#done



