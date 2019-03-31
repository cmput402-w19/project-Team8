import matplotlib.pyplot as plt
import csv
import os 
import pandas as pd

def boxplot(csv_files, col):
    merged_stats = []
    unmerged_stats = []
    
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, sep=",")
        for is_merged in df["PR Merged With"]:
            if(is_merged):
                merged_stats.append(df[col])
            else:
                unmerged_stats.append(df[col])

    merged_boxplot = df.boxplot(column=merged_stats) 
    merged_boxplot.plot()
    plt.savefig("merged_box_plot.png")

    unmerged_boxplot = df.boxplot(column=unmerged_stats) 
    unmerged_boxplot.plot()
    plt.savefig("unmerged_box_plot.png")


boxplot()