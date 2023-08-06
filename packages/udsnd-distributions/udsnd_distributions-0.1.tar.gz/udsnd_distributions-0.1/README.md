# udsnd_distributions package

Summary of the package:

    This package allows the user to create objects from probability distribution classes, which include the Gaussian and Binomial distributions. Several methods have been added to the classes. The package allows the user to instantiate objects from the Gaussian/Binomial classes and do calculations on them, for example reading in a data file and updating the mean/standard deviation of the instantiated object. The package also allows the user to plot the distribution of the data that has been read into the object. Additionally, the user can calculate the probability density/mass at particular values for each of the distributions, with the option of plotting these values for a range of inputs (at which the density/mass is calculated). Below is a summary of all the methods than can be used:

    1. read_data_file(self, file_name): Function to read in data from a txt file. The txt file should have one number (float) per line. The numbers are stored in the data attribute.

    2. calculate_mean(self): Function to calculate the mean of the data set.

    3. calculate_stdev(self, sample=True): Function to calculate the standard deviation of the data set. The user has the option of calculating either a 'Sample' or 'Population' standard deviation. This can be specified using the 'sample' (either True or False) argument in this method.

    4. plot_histogram(self): Function to output a histogram of the instance variable data using matplotlib pyplot library.

    5. pdf(self, x): Probability density function calculator for the gaussian distribution, where x is the point at which the probability density/mass function is to be calculated.

    6. plot_histogram_pdf(self, n_spaces = 50): Function to plot the normalized histogram of the data and a plot of the probability density function along the range. The range calculates the difference between the minimum and maximum values in the Normally distributed data and divides it equally across n_spaces intervals. The probability density function (pdf) is then calculated and plotted for each of the n_spaces intervals. This method can only be used for the Gaussian distribution.

    7. plot_bar_pdf(self): Similar to number 6 above, the Binomial distribution has a method that plots the probability mass function (pmf) at a range of values. The range of values is calculated automatically and depends on the number of samples there are for a particular Binomial distribution.

    8. _add_(self, other): This method allows the user to add (+) two Gaussian or Binomial distributions together and returns the resulting object. For the Binomial distribution, it's important to note that this method only works if we have two objects (Binomial) with the same value for 'p', the probability of an event occurring. If the p values for the separate Binomial objects are different, an error will be raised.

    9. __repr__(self): This method adjusts what is displayed in the console when an object (Gaussian or Binomial) is printed.


# Files

Explanation of the files in the package:

    1. Generaldistribution.py - this file includes the main class from which both thee Gaussian and Binomial classes inherit. This file specifies how an object is instantiated and how the data files are read into the object's 'data' attribute.

    2. Gaussiandistribution.py - this file contains all the methods and additional attributes of the Gaussian class.

    3. Binomialdistribution.py - this file contains all the methods and additional attributes of the Binomial class.

# Installation

pip install udsnd_distributions

