#!/usr/bin/env python3
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Reading data from individual files
group1 = np.loadtxt("group1.txt", skiprows=0)
group2 = np.loadtxt("group2.txt", skiprows=0)

## Transfering data to vertical Vector
# Control Group
g2pre = group2[:,6]

# Experimental Group
g1pre = group1[:,6]

## Fit a normal distribution to the data:
# Control Group
g2mu, g2std = stats.norm.fit(g2pre)

# Experimental Group
g1mu, g1std = stats.norm.fit(g1pre)

## Plot the PDF
# Control Group
x = np.linspace(-10., 35., 100)
p2 = stats.norm.pdf(x, g2mu, g2std)
p2 = p2*21.
plt.plot(x, p2, 'b', linewidth=2, label='Control Group')


# Experiemental Group
p1 = stats.norm.pdf(x, g1mu, g1std)
p1 = p1*20.
plt.plot(x, p1, 'r', linewidth=2, label='Experimental Group')

# Lable and Title for the Graph
title = "Comparision" 
subtitle = "between Control Group Experiemental Group in Pre Test"
plt.xlabel("Marks")
plt.ylabel("Fraction of students in Class")
plt.title(subtitle, fontsize=10)
plt.suptitle(title, fontsize=18)
plt.legend(loc='best')
plt.show()