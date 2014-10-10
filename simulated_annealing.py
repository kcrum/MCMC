import copy
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import twoD_cities as tdc

#
# Perhaps try genetic algorithm next? See: 
#    http://www.theprojectspot.com/tutorial-post/applying-a-genetic-algorithm-to-the-travelling-salesman-problem/5
#

def getEnergy(cities, indices):
    """
    Transform indices to coordinates, then find route length.
    """
    # The tdc.routeLength() function expects an array of coordinates, not an 
    # array of indices. Also don't forget to add starting point (front OR back 
    # is fine).
    route = [cities.coords[ind] for ind in indices + [0]]
    return tdc.routeLength(route)


def getNeighbor(currentsoln):
    """
    Generate a neighboring route to the current solution by randomly selecting
    two cities and swapping their positions.
    """
    # Make deep copy of current solution to fill
    neighborsoln = copy.deepcopy(currentsoln)
    # Get indices of cities to swap.
    indA, indB =  np.random.choice(range(len(currentsoln)), size=2, 
                                   replace=False)
    # Swap values
    newA, newB = neighborsoln[indB], neighborsoln[indA]
    neighborsoln[indA], neighborsoln[indB] = newA, newB

    return neighborsoln

def acceptNeighbor(currentE, neighborE, temp):
    """
    Our acceptance PDF is
       P_move = Bernoulli(exp( (currentE - neighborE)/temp ))
    If neighbor solution is better than current solution (neighE < currE),
    accept neighbor with prob = 1. Otherwise switch to neighbor solution with
    probability P_move.
    """
    if neighborE < currentE:
        return 1
    else:
        return np.random.binomial(1, np.exp((currentE - neighborE)/temp))


def runAnnealing(cities, starttemp = 1e4, endtemp = 1, coolrate = 0.003):
    """
    Take a grid_2d_cities class instance and find its shortest route via
    simulated annealing. We start by setting initial temperature and taking an
    initial solution, then loop until stopping condition (temp <= endtemp) is
    met as follows:
      1) Select a neighbor solution by making a small change to current soln.
      2) Draw from acceptance PDF to determine whether to move to neighbor.
      3) Decrease temperature and continue looping.
    Neighbor solutions are found by taking two random cities on the current 
    solution and swapping them. We use total solution length as our "energy" E
    here. Our acceptance PDF is
       P_move = exp( (E_current - E_neighbor)/temp )
    If neighbor solution is better than current solution (E_neigh < E_curr),
    accept neighbor with prob = 1. Otherwise switch to neighbor solution with
    probability P_move.
    """
    # To save ourselves a little work, we'll fix city 0 as our starting and 
    # ending point. We therefore only look at cities {1,...,ncities-1}.
    currentsoln = range(1,cities.ncities)

    # Find the length (a.k.a. energy) of this first solution. 
    currentE = getEnergy(cities, currentsoln)
    print 'Starting distance: ', currentE
    
    #currentsoln.append(0)
    #cities.drawCities( [cities.coords[ind] for ind in currentsoln] )

    # Create lists and temperature for annealing loop
    energyarr, temparr = [], []
    temp = starttemp

    # Begin annealing
    while temp > endtemp:
        # Generate neighbor solution and find its energy.
        neighborsoln = getNeighbor(currentsoln)
        neighborE = getEnergy(cities, neighborsoln)

        # Should we accept the neighbor solution?
        if acceptNeighbor(currentE, neighborE, temp):
            currentsoln = neighborsoln
            currentE = neighborE

        # Store results
        temparr.append(temp)
        energyarr.append(currentE)

        # Lower the temperature
        temp *= 1 - coolrate

    # currentsoln should now approximately hold the best route.
    return currentsoln, energyarr, temparr

def main(cities):
    simAnnSoln,energyarr, temparr = runAnnealing(cities,100,0.01)

    # Brute force solution won't be computed if ncities > maxBruteN.
    if cities.ncities <= tdc.grid_2d_cities.maxBruteN:
        print '-'*30 + 'Brute force' + '-'*30
        cities.bruteShortest()
        cities.drawCities()

    print '-'*26 + 'Simulated Annealing' + '-'*26
    print 'Lowest energy: ', energyarr[-1], ' Number of iterations: ', \
        len(energyarr)
    cities.drawCities( [cities.coords[ind] for ind in simAnnSoln+[0]] )
    plt.plot(energyarr)
    plt.ylabel('Total distance of route')
    plt.xlabel('Iterations')
    plt.show()

if __name__ == '__main__':
    # Put 8 cities on a 12 x 12 grid
    cities = tdc.grid_2d_cities(20,12,12)
    
    main(cities)
