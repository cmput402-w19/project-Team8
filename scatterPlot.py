import matplotlib.pyplot as plt
import csv
import os 
import pandas as pd
import numpy as np

red = "#DC143C"
green = "#32CD32"
colors = [green, red]

def prep_csv_data(csv_files):
    merged_prs_x = []
    unmerged_prs_x = []
    merged_prs_y = []
    unmerged_prs_y = []

    merged_counts = 0
    merged_counts_below = 0
    unmerged_counts = 0
    unmerged_counts_above = 0
    counter = 0

    for csv_file in csv_files:
        data_frames = pd.read_csv(csv_file, sep=",") 

        x_data_frame = data_frames["Test Case Density Difference"] 
        y_data_frame = data_frames["Assert Test Cases Difference"]
        merged = data_frames["PR Merged With"]



        for i in range (len(x_data_frame)):
            counter += 1
            if merged[i] == "Merged":
                merged_prs_x.append(x_data_frame[i])
                merged_prs_y.append(y_data_frame[i])
                if((x_data_frame[i] >= 0) & (y_data_frame[i] >= 0)):
                    merged_counts += 1
                elif((x_data_frame[i] < 0) & (y_data_frame[i] < 0)):
                    merged_counts_below += 1 
            else:
                if((x_data_frame[i] < 0) & (y_data_frame[i] < 0)):
                    unmerged_counts += 1
                elif((x_data_frame[i] >= 0) & (y_data_frame[i] >= 0)):
                    unmerged_counts_above += 1
                unmerged_prs_x.append(x_data_frame[i])
                unmerged_prs_y.append(y_data_frame[i])
    data = ((merged_prs_x, merged_prs_y), (unmerged_prs_x, unmerged_prs_y))
    # print(x_data_frame[:10])
    # print(1000*x_data_frame[:10])
    # data = (unmerged_prs_x * 1000, unmerged_prs_y * 1000)
    # print(data)
    groups = ("merge", "unmerged")
    # groups = ("unmerged")
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, facecolor="1.0")
    x = np.linspace(min(x_data_frame), max(x_data_frame), 100)
    y = 0*x
    plt.plot(x, y)
    for data, color, group in zip(data, colors, groups):
        header = group
        x, y = data
        ax.scatter(x, y, alpha=0.8, c=color, edgecolors="none", label=group)          

    x = np.linspace(min(min(unmerged_prs_x), min(merged_prs_x)), max(max(unmerged_prs_x), max(merged_prs_x)), 100)
    y = 0*x
    x2 = 0*y
    y2 = np.linspace(min(min(unmerged_prs_y), min(merged_prs_y)), max(max(unmerged_prs_y), max(merged_prs_y)), 100)
    
    print(merged_counts, "merged counts in quad1")
    print(unmerged_counts_above, "unmerged commits in quad1")
    print(merged_counts_below, "merge commits in quad 3")
    print(unmerged_counts, "unmerged counts in quad 3\n")
    print(counter, "total rows")


    plt.title("title")
    plt.plot(x, y, "-b")
    plt.plot(x2, y2, "-b")

    plt.xlabel("test case density diff")
    plt.ylabel("assert test case diff")
    plt.savefig("./results/plots/overall_scatter_plot.png")
    plt.close()
    
def scatter_plot_repo(csv_files):

    for csv_file in csv_files:
        data_frames = pd.read_csv(csv_file, sep=",") 
        merged_prs_x = []
        unmerged_prs_x = []
        merged_prs_y = []
        unmerged_prs_y = []

        x_data_frame = data_frames["Test Case Density Difference"]
        y_data_frame = data_frames["Assert Test Cases Difference"]
        merged = data_frames["PR Merged With"]
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
            ax.scatter(x, y, alpha=0.8, c=color, edgecolors="none", label="unmerged")       
      
         
        x = np.linspace(min(x_data_frame), max(x_data_frame), 100)
        y = 0*x
        x2 = 0*y
        y2 = np.linspace(min(y_data_frame), max(y_data_frame), 100)

        plt.title(csv_file)
        plt.plot(x, y, "-b")
        plt.plot(x2, y2, "-b")

        plt.xlabel("test case density diff")
        plt.ylabel("assert test case diff")

        fileName = csv_file.replace(".csv","")

        plt.savefig("./results/plots/{}_scatterplot.png".format(fileName))
        plt.close()


def main():
    csv_path = "./results/test_density_export/"
    csv_files = []
    for filename in  os.listdir(csv_path):
        csv_files.append(csv_path+filename)
    prep_csv_data(csv_files)
main()