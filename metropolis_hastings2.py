"""
 Metropolis-Hastings algorithm is an MCMC process that allows you to estimate
 a PDF P(x) if you have some function f(x) which is proportional to P(x). You
 need to also choose a proposal density Q(y|z). If Q(y|z) is symmtric, i.e.
 Q(y|z) =  Q(z|y), then we have just the Metropolis algorithm (a special case
 of M.-H. algorithm).

 The algorithm starts when some initial x0 is chosen. We then draw x' from
 Q(x'|x0). Calculate r1 = f(x')/f(x0) and r2 = Q(x0|x')/Q(x'|x0). Note that if
 Q is symmetric, r2 is always 1. We choose a new state x1 by the following:
   1) If r1*r2 >= 1, then x1 = x'.
   2) Otherwise, x1 = x' with probability r1*r2, and x1 = x0 with probability
      1-r1*r2.
 Repeat the above for x1. We do this for many iterations (burn-in), then
 discard the values. We continue from the last burn-in point, taking all
 accepted values as a sample of P(x).

 Often a Gaussian N(x;y,sigma) is chosen for Q. Note that N(z;y,s) = N(y;z,s).
 The proposal density most efficiently proposes values when P~Q.

"""
import numpy as np
import scipy.stats as st
import scipy.optimize as sciop
import scipy.integrate as scint
import matplotlib.pyplot as plt

sigma=1.
propsigma=3.
mean=-1.
iterations=10000
nburn = 30
startx = 0.

# We can use an improperly normalized Gaussian as our distribution f(x)
dist = lambda x: np.exp( -(x - mean)**2/(2.*sigma**2) )

# This is a messier, bimodal-looking distribution. We'll set it to zero outside
# of its two real roots.
fnc2 = lambda x: -(x)**4 - 3*(x)**3 + 5
root1, root2 = sciop.brentq(fnc2, -4, -2), sciop.brentq(fnc2, -2, 2)

def dist2(x0):
    x = 0
    if isinstance(x0, float):
        x = np.array([x0])
    else:
        x = np.array(x0)
    resarr = np.empty(len(x))

    for i in range(len(x)):
        if x[i] > root1 and x[i] < root2:
            resarr[i] = fnc2(x[i])
        else:
            resarr[i] = 0.
    return resarr

def proposalratio(prevx, nextx):
    # Find Q(nextx|prevx).
    probnext = st.norm.pdf(nextx, loc=prevx, scale=propsigma)
    # Find Q(prevx|nextx).
    probprev = st.norm.pdf(prevx, loc=nextx, scale=propsigma)
    # Return Q(prevx|nextx)/Q(nextx|prevx).
    return probprev/probnext

def distributionratio(prevx, nextx, func):
    if func(prevx) == 0:
        print('Exiting: prevx = %s' % prevx)
        exit()
    return func(nextx)/func(prevx)

def histresults2(arrburn, arrdist):
    nbins = iterations/100
    bins = np.linspace(mean - 3*sigma, mean + 3*sigma, nbins)
    plt.hist(arrburn, bins, label='Burn-in')
    plt.hist(arrdist, bins, alpha=0.5, label='Distribution')
    # Prepare true distribution plot
    binwidth = (6*sigma)/nbins
    histnorm = binwidth*iterations
    x = np.linspace(mean - 3*sigma, mean + 3*sigma, 100)
    dist2int = scint.quad(dist2, -4, 2)
    print('dist2int: %s' % dist2int[0])
    plt.plot(x, (histnorm/dist2int[0])*dist2(x), label='Truth')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    prevx = startx
    arrburn = np.empty(nburn)
    arrdist = np.empty(iterations)

    for n in range(iterations + nburn):
        # This is the proposal draw from Q(.|prevx)
        nextx = st.norm.rvs(loc=prevx, scale=propsigma)
        # This is only useful when calling dist2!
        while nextx <= root1 or nextx >= root2:
            nextx = st.norm.rvs(loc=prevx, scale=propsigma)

        rprop = proposalratio(prevx, nextx)
        rdist = distributionratio(prevx, nextx, dist2)

        if rprop*rdist >= 1:
            prevx = nextx
        else:
            if np.random.binomial(1, rprop*rdist) == 1: prevx = nextx

        if n < nburn:
            arrburn[n] = prevx
        else:
            arrdist[n-nburn] = prevx

    histresults2(arrburn, arrdist)
