
import matplotlib.pyplot as plt
import csv
import os 
import pandas as pd

red = "#DC143C"
green = "#32CD32"
colors = [red, green]

def prep_csv_data(csv_file):

    data_frames = pd.read_csv(csv_file, sep=",") 

    x_data_frame = data_frames["Test Case Difference"]
    y_data_frame = data_frames["Test Cases Difference"]
    merged = data_frames["PR Merged With"]

    merged_prs_x = []
    unmerged_prs_x = []
    merged_prs_y = []
    unmerged_prs_y = []

    for i in range (len(x_data_frame)):
        if merged[i] == "Merged":
            merged_prs_x.append(x_data_frame[i])
            merged_prs_y.append(y_data_frame[i])
        else:
            unmerged_prs_x.append(x_data_frame[i])
            unmerged_prs_y.append(y_data_frame[i])
    data = ((merged_prs_x, merged_prs_y), (unmerged_prs_x, unmerged_prs_y))

    groups = ("merge", "unmerged")
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, facecolor="1.0")
    for data, color, group in zip(data, colors, groups):
        
        x, y = data
        print(len(x), len(y))
        ax.scatter(x, y, alpha=0.8, c=color, edgecolors="none", label=group)          
    plt.show()
    plt.savefig("./scatter.png")
    plt.close()
    
def main():
    # for csv_file in csv_files:
    prep_csv_data("identity_cache.csv")
main()