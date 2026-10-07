""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
#from numba import njit

# Exc1
def approximate_pi(n):
    #Approximera π med n = {1000, 10000, 100000}. Skapa figurer för dessa värden på n.
    #Skriv ut antalet punkter n.
    #2. Skriv ut och returnera approximationen av π ≈ 4nc/n.
    #3. Producera en png-fil som visar alla punkter inne i cirkeln som röda prickar och
    # punkterna utanför cirkeln som blå prickar (som i Figur 2).
    x,y = random.uniform(0,1), random.uniform(0,1)
    in_circle = []
    outside_circle = []
    for i in range (n):
        x,y = random.uniform(-1,1), random.uniform(-1,1)
        if (x**2 + y**2) <= 1:
            in_circle.append([x,y])
        else:
            outside_circle.append([x,y])
    pi = 4*len(in_circle)/n

    #Plotting
    plt.figure(figsize=(6,6))
    for i in range(len(in_circle)):
        plt.plot(in_circle[i][0], in_circle[i][1], 'ro', markersize=1)
    for i in range(len(outside_circle)):
        plt.plot(outside_circle[i][0], outside_circle[i][1], 'bo', markersize=1)
    plt.xlabel(f'Plot for n = {n} pi = {pi}', fontsize=10)
    plt.savefig(f'plot_n_{n}.png')
    plt.show()
    return (pi)

# Exc2, approximation

def is_inside_circle(point):
    squares = [i**2 for i in point]

    if(sum(squares) <= 1):
        return True
    else:
        return False

def sphere_volume(n, d): 
    # n is the number of points
    # d is the number of dimensions of the sphere
    points_list = [[random.uniform(-1,1) for i in range(0,d)] for j in range(0,n)] #list comprehension
    in_circle = filter(is_inside_circle, points_list) # filter

    zip_tal=list(zip(range(len(points_list)),points_list)) #zip
    outside_circle_index = [x[0] for x in zip_tal if not is_inside_circle(x[1])] #list comprehension
    outside_circle = [points_list[i] for i in outside_circle_index]

    volume = len(list(in_circle))/n *(2**d) #Volume of d-dimensional sphere
    return(volume)


#Exc2, real value
def hypersphere_exact(d):
    # n is the number of points
    # d is the number of dimensions of the sphere 
    V_d = (m.pi**(d/2))/m.gamma(d/2 + 1) #True volume of d-dimensional sphere
    return V_d

#Exc3: numba version
def sphere_volume_numba(n:int, d:int)->float:
    # n is the number of points

    # d is the number of dimensions of the sphere
    #np is the number of processes
    return

#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
    return 
    
def main():
    # Exc1
    '''dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)'''

    # Exc2
    n = 100000
    d = 2
    print("Approx volume = ", sphere_volume(n, d))
    print(f"Actual volume of {d} dimensional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    print("Approx volume = ", sphere_volume(n, d))
    print(f"Actual volume of {d} dimensional sphere = {hypersphere_exact(d)}")
'''
    # Exc3
    n = 1000000
    d = 11
    for i in range(3):
        start = pc()
        sphere_volume(n, d)
        stop = pc()
        print(f"Exc3: Sequential time of {d} and {n}: {stop-start}")
    print("What is numba time?")

    # Exc4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
'''
    
    

if __name__ == '__main__':
	main()
