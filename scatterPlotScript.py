
import matplotlib.pyplot as plt
import csv
import os 
import pandas as pd

# N = 500
# x = np.random.rand(N)
# y = np.random.rand(N)
# colors = (0,0,0)
# area = np.pi*3
 
# # Plot
# plt.scatter(x, y, s=area, c=colors, alpha=0.5)
# plt.title('Scatter plot pythonspot.com')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()
# https://pythonspot.com/matplotlib-scatterplot/
red = "#DC143C"
green = "#32CD32"
colors = [red, green]

def prep_csv_data(csv_file):
    data_frames = pd.read_csv(csv_file, ",") 
    x_data_frame = data_frames["Test Case Difference"]
    y_data_frame = data_frames["Test Cases Difference"]
    merged = data_frames["PR Merged With"]

    merged_prs_x = []
    unmerged_prs_x = []
    merged_prs_y = []
    unmerged_prs_y = []

    for i in range (len(x_data_frame)):
        if merged[i]":
            merged_prs_x.append(x_data_frame[i])
            merged_prs_y.append(y_data_frame[i])
        else:
            merged_prs_y.append(x_data_frame[i])
            unmerged_prs_y.append(y_data_frame[i])
    data = ((merged_prs_x, merged_prs_y), (unmerged_prs_x, unmerged_prs_y))
    groups = ("merge", "unmerged")

    for data, color, group in zip(data, colors, groups):
        x, y = data
        sp = ax.scatter(x, y, alpha=0.8, c=color, edgecolors="none", label=group)          
        sp.plot()
        plt.savefig("./scatter.png")
        plt.close()
    


def graph_scatter_plot(csv_files):
    pass
    # num_repos = len(x)

    # for i in range(num_repos):
    #     plt.scatter(x[0], y[0], s=areas[0], alpha=0.5)
    #     plt.xlabel("assert cases per kloc")
    #     plt.ylabel("test cases per kloc")

def main():
    # for csv_file in csv_files:
    prep_csv_data("diaspora.csv")
main()