import sys
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

        self.xarray, self.yarray = [], []
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
                if xval in self.xarray and yval in self.yarray:
                    while xval in self.xarray and yval in self.yarray:
                        xval = int(np.floor(np.random.uniform(0,self.xlength)))
                        yval = int(np.floor(np.random.uniform(0,self.ylength)))

                self.xarray.append(xval)
                self.yarray.append(yval)

    def drawCities(self):
        fig = plt.figure()
        ax = fig.gca()
        ax.set_xticks(np.arange(-1, self.xlength))        
        ax.set_yticks(np.arange(-1, self.ylength))
        plt.scatter(self.xarray, self.yarray)
        plt.xlim(-0.5, self.xlength-0.5)
        plt.ylim(-0.5, self.ylength-0.5)
        # Add rectangle
        ax.add_patch(Rectangle((0,0),self.xlength-1,self.ylength-1,
                               alpha=0.3, color='gray')) 
        plt.grid()
        plt.show()
