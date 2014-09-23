import itertools, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

np.random.seed(3)

# Put cities on random integer vertices of [0, ncities-1] x [0, ncities-1] grid
# by default. You may also pass xlength and ylength
# Each city has a unique vertex.
class grid_2d_cities():
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

        self.coords = []
        self.generateCities()    

    # Put ncities on a [0, xlength-1] x [0, ylength-1] integer grid.
    def generateCities(self):
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

    # Draw cities as they appear on the grid.
    def drawCities(self):
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
        plt.show()

    # Calculate the distance between cities at ind1 and ind2 of the coordinate
    # array.
    def distance(self, ind1, ind2):
        if ind1 >= self.ncities or ind2 >= self.ncities:
            print 'Indices must integers be less than', self.ncities
        else: 
            return np.sqrt( (self.coords[ind1][0]-self.coords[ind2][0])**2 +
                            (self.coords[ind1][1]-self.coords[ind2][1])**2 )

    # Brute force shortest route
    def bruteShortest(self):
        if self.ncities > 7:
            print 'There are too many cities to find a solution by brute force.'
            print 'ncities = %s, which means %s possible paths.' %\
                (self.ncities, np.math.factorial(self.ncities-1))
        else:
            print 'Put brute force algorithm here.'
