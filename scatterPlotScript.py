
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


    for csv_file in csv_files:
        data_frames = pd.read_csv(csv_file, sep=",") 

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
    header = None
    x = np.linspace(min(x_data_frame), max(x_data_frame), 100)
    y = 0*x
    plt.plot(x, y)
    for data, color, group in zip(data, colors, groups):
        header = group
        x, y = data
        ax.scatter(x, y, alpha=0.8, c=color, edgecolors="none", label=group)         
    # x = np.linspace(min(x_data_frame), max(x_data_frame), 100)
    # y = 0*x
    # x2 = 0*y
    # y2 = np.linspace(min(y_data_frame), max(y_data_frame), 100)
    x = np.linspace(min(min(unmerged_prs_x), min(merged_prs_x)), max(max(unmerged_prs_x), max(merged_prs_x)), 100)
    y = 0*x
    x2 = 0*y
    y2 = np.linspace(min(min(unmerged_prs_y), min(merged_prs_y)), max(max(unmerged_prs_y), max(merged_prs_y)), 100)

    plt.title("title")
    plt.plot(x, y, "-b")
    plt.plot(x2, y2, "-b")

    plt.xlabel("test case density diff")
    plt.ylabel("assert test case diff")
    plt.show()
    plt.savefig("./scatter.png")
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

        plt.show()
        plt.savefig("./scatter.png")
        plt.close()


def main():
    # for csv_file in csv_files:
    csv_files = ["android.csv", "blueflood.csv", "brightspot-cms.csv", "expertiza.csv",
        "heroku-buildpack-ruby.csv", "identity_cache.csv", "liquid.csv", "querydsl.csv",
        "rspec-core.csv", "rspec-mocks.csv", "samson.csv", "Singularity.csv", "travis-core.csv"]
    prep_csv_data(csv_files)
    # scatter_plot_repo(csv_files)
main()