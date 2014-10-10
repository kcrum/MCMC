import itertools, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


randomseed = 1
np.random.seed(randomseed)
debug = False

def distance(coord1, coord2):
    """
    Generic n-dimensional Euclidean distance function.
    """
    if len(coord1) != len(coord2):
        print 'Coordinates must be of same dimension. Returning 0.'
        return 0
    diffsq = [(el[0] - el[1])**2 for el in zip(coord1,coord2)]
    return np.sqrt(np.array(diffsq).sum())

def routeLength(arr):
    """
    Calculate distance of array in order, connecting final element to first 
    element.
    """
    if len(arr) <= 1:
        print 'Array too short. Exiting with route length = 0.'
        return 0

    totaldist = 0 
    prevelem = arr[-1]
    for elem in arr:
        totaldist += distance(prevelem, elem)
        prevelem = elem

    return totaldist

###############################################################################
###############################################################################
class grid_2d_cities():
    """
    Put cities on random integer vertices of [0, ncities-1] x [0, ncities-1] 
    grid by default. You may also pass xlength and ylength. Each city has a
    unique vertex.
    """

    # If there are more than 9 cities, the brute force algorithm becomes too 
    # slow. For n cities, we search (n-1)! routes.
    maxBruteN = 9

    def __init__(self, *args):
        if len(args) == 0:
            print 'Must pass at least one integer to constructor. Exiting.'
            sys.exit()
            
        self.ncities = int(np.ceil(args[0]))
        self.xlength = self.ylength = self.ncities
        if len(args) > 1:
            self.xlength = int(np.ceil(args[1]))
        if len(args) > 2:
            self.ylength = int(np.ceil(args[2]))

        # Array to store coordinate pairs
        self.coords = []
        # Array to store brute force shortest route
        self.bruteshortest = []
        self.generateCities()    

    def generateCities(self):
        """
        Put ncities on a [0, xlength-1] x [0, ylength-1] integer grid.
        """
        if self.ncities > self.xlength*self.ylength:
            print 'The product xlength*ylength must be greather than ncities.'
            print 'Cities won\'t generate until this happens.'
        else:
            for i in xrange(self.ncities):
                xval = int(np.floor(np.random.uniform(0,self.xlength)))
                yval = int(np.floor(np.random.uniform(0,self.ylength)))
                # Enure point is unique
                if (xval,yval) in self.coords:
                    while (xval,yval) in self.coords:
                        xval = int(np.floor(np.random.uniform(0,self.xlength)))
                        yval = int(np.floor(np.random.uniform(0,self.ylength)))
                # Add point to coordinate array
                self.coords.append((xval,yval))


    def drawCities(self, route = []):
        """
        Draw cities as they appear on the grid. If a route is passed, this will
        be drawn as a collection of arrows linking the cities.
        """
        # If no route was passed (and bruteshortest has been found), add arrows
        # showing bruteshortest path.
        if not route and self.bruteshortest:
            route = self.bruteshortest
        fig = plt.figure()
        ax = fig.gca()
        ax.set_xticks(np.arange(-1, self.xlength))        
        ax.set_yticks(np.arange(-1, self.ylength))
        # Unpack coordinate pairs
        xarr, yarr = zip(*self.coords)
        # Plot coordinates
        plt.scatter(xarr, yarr)
        plt.xlim(-0.5, self.xlength-0.5)
        plt.ylim(-0.5, self.ylength-0.5)
        # Add rectangle
        ax.add_patch(Rectangle((0,0),self.xlength-1,self.ylength-1,
                               alpha=0.3, color='gray')) 
        plt.grid()
        # Add arrows for a route, if route exists
        if route:
            self.addArrows(ax, route)
        plt.show()

    def addArrows(self, ax, route):
        """
        Add arrows to plot showing the specified route. This function does the 
        array wrap-around for you, so no need to manually add route[0] to both
        the front end and the back end of the route.
        """
        print "Route length:", routeLength(route)
        # Start at last point in route so the arrows wrap all the way around.
        prevpt = route[-1]
        for pt in route:
            dx, dy = pt[0]-prevpt[0], pt[1]-prevpt[1]
            scale = 1 - 0.3/np.sqrt(dx**2 + dy**2)
            ax.arrow(prevpt[0], prevpt[1], scale*dx, scale*dy,
                     head_width=0.1)
            prevpt = pt

    def cityDistance(self, ind1, ind2):
        """
        Calculate the distance between cities at ind1 and ind2 of the 
        coordinate array.
        """
        if ind1 >= self.ncities or ind2 >= self.ncities:
            print 'Indices must integers be less than', self.ncities
        else: 
            return np.sqrt( (self.coords[ind1][0]-self.coords[ind2][0])**2 +
                            (self.coords[ind1][1]-self.coords[ind2][1])**2 )
        
    # Brute force shortest route
    def bruteShortest(self):
        """
        We are only interested in unique routes, i.e. the same path with a
        different starting point or directionality (clockwise vs. 
        counterclockwise) should not be considered. For example there are 6
        different permutations for three cities, but each of these 6 
        permutations has the same total distance. 
        
        To reduce redundacy, for n cities labeled 0 to n-1, we demand that
        city 0 be the starting point. There are still a factor of 2 too 
        many routes, as reversals lead to identical distances (e.g. for 5 
        cities labeled 0 to 4, [0,1,2,3,4] has the same distance as 
        [0,4,3,2,1]). 
        """
        if self.ncities > grid_2d_cities.maxBruteN:
            print 'There are too many cities to find a brute force solution.'
            print 'ncities = %s, which means %s possible paths.' %\
                (self.ncities, np.math.factorial(self.ncities-1))            
        else:
            mindist = -1
            mindistindices = []
            # Loop over all permutations of {1,...,ncities-1}
            for perm in itertools.permutations(range(1,self.ncities)):
                # Store each permutation of indices in an array.
                indices = [ind for ind in perm]
                # Don't forget to add starting point (front OR back is fine)
                indices.append(0)
                newroute = [self.coords[ind] for ind in indices]
                newdist = routeLength(newroute)

                # This is for debugging. 
                if debug: print 'indices: ', indices

                # This is for debugging. 
                if debug and newdist == mindist:
                    print 'Redundant minimum routes:'
                    print mindistindices, ' and '
                    print indices

                # If (shorter path) or (first iteration) (i.e. when 
                # mindistindices is empty; this will be minimum no matter 
                # what.)
                if newdist < mindist or not mindistindices:                    
                    mindist = newdist
                    mindistindices = indices
                    
            self.bruteshortest = [self.coords[ind] for ind in mindistindices]
            print 'Brute force solution has length: ', mindist

if __name__ == '__main__':
    mycities = grid_2d_cities(8,12,12)
    mycities.bruteShortest()
    mycities.drawCities()
