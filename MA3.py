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
from numba import njit
import numpy as np

# Exc1
def approximate_pi(n):
    #Approximera π med n = {1000, 10000, 100000}. Skapa figurer för dessa värden på n.
    #Skriv ut antalet punkter n.
    #2. Skriv ut och returnera approximationen av π ≈ 4nc/n.
    #3. Producera en png-fil som visar alla punkter inne i cirkeln som röda prickar och
    # punkterna utanför cirkeln som blå prickar (som i Figur 2).
    #x,y = random.uniform(0,1), random.uniform(0,1)
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
def hypersphere_exact(n,d):
    # n is the number of points
    # d is the number of dimensions of the sphere 
    V_d = (m.pi**(d/2))/m.gamma(d/2 + 1) #True volume of d-dimensional sphere
    return V_d

#Exc3: numba version
@njit
def is_inside_circle_numba(point):
    sum_squares = 0.0 #testa 0 sen
    for i in range(0,len(point)):
        sum_squares += point[i]**2
    
    if(sum_squares <= 1):
        return True
    else:
        return False
    
@njit
def sphere_volume_numba(n:int, d:int)-> float:
    # n is the number of points
    # d is the number of dimensions of the sphere
    in_circle = 0
    for i in range (0, n):
        point = [np.random.uniform(-1,1) for i in range(0,d)]
        if is_inside_circle_numba(point):
            in_circle += 1
    
    volume = in_circle/n *(2**d) #Volume of d-dimensional sphere
    return(volume)

#Exc4: parallel code - parallelize actual computations by splitting data

def sphere_volume_wrapper(args):
    return sphere_volume(*args)


def sphere_volume_parallel1(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
    result = 0
    with future.ProcessPoolExecutor() as ex:
        p = [(n,d) for i in range(0,np)]
        #results = ex.map(sphere_volume,p)
        #results = ex.submit(sphere_volume,n,d)
        futures = [ex.submit(sphere_volume, *args) for args in p]
        results = [f.result() for f in futures]
        summ = sum(results)/np
    return (summ)

def sphere_volume_parallel(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
    result = 0
    with future.ProcessPoolExecutor() as ex:
        p = [(n,d) for i in range(0,np)]
        results = list(ex.map(sphere_volume_wrapper, p))
        summ = sum(results)/np
    return (summ)


def sphere_volume_parallel_numba(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
    result = 0
    with future.ProcessPoolExecutor() as ex:
        p = [(n,d) for i in range(0,np)]
        results = ex.map(sphere_volume_numba,p)
    return (results)
    
def main():
    '''
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    # Exc2
    n = 100000
    d = 2
    print("Approx volume = ", sphere_volume(n, d))
    print(f"Actual volume of {d} dimensional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    print("Approx volume = ", sphere_volume(n, d))
    print(f"Actual volume of {d} dimensional sphere = {hypersphere_exact(n,d)}")

    # Exc3
    n = 1000000
    d = 11
    for i in range(3):
        start = pc()
        sphere_volume(n, d)
        stop = pc()
        print(f"Exc3: Sequential time of original {d} and {n}: {stop-start}")
    for i in range(3):
        start = pc()
        sphere_volume_numba(n, d)
        stop = pc()
        print(f"Exc3: Sequential time of numba {d} and {n}: {stop-start}")
    
    # Exc4
    
    print("Starting program")
    n = 1000000
    d = 11
    np = 10
    start = pc()
    for i in range (0,np):
        result = sphere_volume(n, d)
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")
    '''
    n = 1000000
    d = 11
    np = 10
    start = pc()
    result = sphere_volume_parallel(n,d, np)
    stop = pc()
    print(f"What is parallel time? It is {stop-start}")
    
    n = 1000000
    d = 11
    np = 10
    start = pc()
    result = sphere_volume_parallel_numba(n,d, np)
    stop = pc()
    print(f"What is parallel time with numba? It is {stop-start}")
    
    

if __name__ == '__main__':
    main()