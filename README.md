# Data-analysis-Engineering-Project
The aim of the project to use modified Newtonian dynamics to describe new data for rotation curves of galaxies from astronomical observations by Lelli et al. (The Astronomical Journal, 152 (2016) 157).


The problem of the rotation curve as an anomaly on the galactic scale raises the question of the validity of
theories trying to explain this phenomenon. One of them, next to dark matter, is the theory of modified Newtonian
dynamics - MOND. The paper presents the results and a description of the method of its use to describe the data for the
rotation curves of 175 galaxies from astronomical observations, made with the Spitzer telescope by the team of F. Lelli,
S.S. McGaugh and J.M. Schombert, published in The Astronomical Journal (152 (2016) 157). For this purpose, a
program was written in Python using the Scikit-learn, SciPy and Matplotlib libraries. 

The program uses the method of finding the minimum of the mean squared error function to find the optimal parameter a 0 of the MOND model for each of
the galaxies in such a way that it overlaps as best as possible with observational data. The obtained results indicate that
the fit of the model to the observational data is in most cases correct, and small deviations are within the assumed
measurement error. In 4 cases, a poor fit is due to too little data, the rest, such as the galaxy UGC06973, may indicate
weak data or a wrong fitting method in this case. This does not exclude that the MOND theory describes rotation curves
well and has the potential to become a universally accepted model for galaxy description.
