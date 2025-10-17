import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.pyplot as plt
#import imageio
from matplotlib.cm import ScalarMappable
import pickle
import sys
from matplotlib.lines import Line2D

#https://matplotlib.org/3.1.0/tutorials/colors/colormap-manipulation.html
#custom color map: set desired map (either grainbow or viridis here) to the newcolors
levels = 200
grainbow = cm.get_cmap('gist_rainbow', levels)
viridis = cm.get_cmap('viridis', levels)
newcolors = viridis(np.linspace(0, 1, levels))

#uncomment to add white when 0
#white = np.array([1, 1, 1, 1])
#newcolors[:2, :] = white
newcmp = ListedColormap(newcolors)
chosencmap = grainbow

outFolder = "Plots/"
nPhases = 29
withEDM = False

#load in pkled decay probs, at chosen phase index degrees
#phase index goes from 0-29 and cover 0 -> 2pi
#so for example phase index 7 is at phi = (7/29)*2pi ~ pi/2
inFolder = "InputFiles"
filename = "G2"
phaseIndex = 7

#pick your lambda slices, can just use [0.6] for single plot,
#also make stems for fancy labels later on
#sliceLs = [0.2 + i*(0.01) for i in range(0,73)]
sliceLs = [0.6]
lamStem = r'$\lambda$'
momStem = r'$p_{e^{+}}$'
phiStem = r'$\phi$'
piStem = r'$\pi$'

#construct the input filename
fn = f"{inFolder}/{filename}_{phaseIndex:02d}.pkl"

#now load in the X,Y,Z from the input file
# X: the fractional (i.e. divided by maximum energy) lab frame energy of the decay positrons: labelled as lambda: unitless
# Y: the lonitidunal angle of the decay positrons: labelled as theta_L: in mrad
# Z: the probability density of this lambda and tehta_L : unitless
with open(fn, "rb") as f:
    X,Y,Z = pickle.load(f)

    #make 2D plot of X, Y and Z
    plt.clf()
    plt.xlabel(f'Fractional Lab Frame Energy ({lamStem})')
    plt.ylabel(r'Longitudinal Angle ($\theta_L$) [rads]')
    plt.title(f'Decay Probability {phiStem}={phaseIndex/29:.2f}{piStem}')
    
    qcs = plt.contourf(X,Y,Z, levels, cmap = newcmp)
    cbar = plt.colorbar( ScalarMappable(norm=qcs.norm, cmap=qcs.cmap) )#, ticks=range(vmin, vmax+5, 5))   )
    cbar.ax.set_ylabel(r'Probability Density')
    outname = outFolder + f"ProbabilityDensity.png"
    plt.savefig(outname)

    #lambda and theta are read in from the file, same for all data
    l = X[0]
    theta = Y[:,0]

    #example of how to take a slice in energy and plot it. Loops over all the energies is sliceL
    for sliceL in sliceLs:

        #argmin finds the index of the minimum of the argument
        # in this case the index of the nearest value in array l of sliceL 
        lindex = np.argmin(np.abs(sliceL-l))
        #have to transpose it for reasons i forget, but probably how numpy deals with arrays
        z = Z[:,lindex].transpose()

        #plot the probability as a function of the angle, for the given lambda
        plt.clf()
        plt.xlim([-75, 80])
        plt.title(f"{lamStem} = {sliceL:.2f}")
        plt.plot(theta*1000, z, label="100% acc.")
        plt.xlabel(r"Longitudinal Angle ($\theta_{L}$) [mrad]")
        plt.ylabel("Probability density")
        plt.legend()
        outname = outFolder + f"theta_{sliceL:.2f}.png"
        plt.savefig(outname)
