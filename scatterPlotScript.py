
import matplotlib.pyplot as plt
import csv
import os 
import pandas as pd

N = 500
x = np.random.rand(N)
y = np.random.rand(N)
colors = (0,0,0)
area = np.pi*3
 
# Plot
plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.title('Scatter plot pythonspot.com')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
# https://pythonspot.com/matplotlib-scatterplot/
def graph_scatter_plot(x, y, s):
    pass
