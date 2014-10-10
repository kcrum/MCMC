# MCMC Code Snippets

## Metropolis-Hastings
The metropolis_hastings algorithms simply estimate a distribution using the Metropolis-Hastings algorithm. The two different versions just estimate two different distributions.

## 2-D Cities
The twoD_cities class generates an arbitrary number of cities on a 2-D grid of user-specified size. The class can find a brute-force solution to the traveling salesman problem too, but there's a hardcoded cap for the maximum number of cities for which it will implement the brute-force solution. The class also plots the cities and any path specified by the user (if a brute force solution has been found, this gets plotted by default).

## Simulated Annealing
This solves the traveling salesman using a simple simulated annealing algorithm. Running main() will find a solution and compare it to the brute force solution, if the brute force solution is allowable (brute force solver is capped since number of paths grows as (n-1)!).