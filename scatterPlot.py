import matplotlib.pyplot as plt
import csv
import os 
import pandas as pd
import numpy as np

red = "#DC143C"
green = "#32CD32"
colors = [green, red]

def build_overall_scatterplot(csv_files, graph_title, save_flag, file_name):
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
    
    print(merged_counts, "merged counts in quad 1")
    print(unmerged_counts_above, "unmerged commits in quad 1")
    print(merged_counts_below, "merge commits in quad 3")
    print(unmerged_counts, "unmerged counts in quad 3\n")
    print(counter, "total rows")
    print("unmerged PR % inside  quad 1: ", (unmerged_counts_above/len(unmerged_prs_x)))
    print("merged PR in quad 1 %: ", (merged_counts / len(merged_prs_x)))
    print("unmerged PR % inside  quad 3: ", (unmerged_counts/len(unmerged_prs_x)))
    print("merged PR in quad 3: ", (merged_counts_below/len(merged_prs_x)))
    

    plt.title(graph_title)
    plt.plot(x, y, "-b")
    plt.plot(x2, y2, "-b")

    plt.xlabel("test case density diff")
    plt.ylabel("assert test case diff")
    if(save_flag):
        plt.savefig("./results/plots/"+file_name)

    plt.title("Focused Scatterplot of All PRs")
    plt.xlim(-5, 8)
    plt.ylim(-9, 13)
    # plt.show()
    if(save_flag):
        plt.savefig("./results/plots/focused_"+file_name)
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
    type3_csv_files = ["jedis", "capybara", "adhearsion", "expertiza", "prawn","graphite", "blacklight", "geoserver", "omnibus", "shoulda-matchers"]

    for i in range(len(type3_csv_files)):
        type3_csv_files[i] = csv_path + type3_csv_files[i] + ".csv"
        
    build_overall_scatterplot(type3_csv_files, "PRs With Testing Contribution Policies", True, "contribution_policies_scatter_plot.png")

    type12_csv_files = [] 

    print("#####################################")
    print("Overall of all 30 repos")
    for filename in  os.listdir(csv_path):
        csv_files.append(csv_path+filename)
        if csv_path+filename not in type3_csv_files:
            type12_csv_files.append(csv_path+filename)
    build_overall_scatterplot(csv_files, "Scatterplot of All PRs", True, "overall_scatter_plot.png")

    print("######################################")
    print("Overall of type 1 & 2 repos")
    build_overall_scatterplot(type12_csv_files, "PRs Without Testing Contribution Policies", True, "no_contribution_policies_scatter_plot.png")
main()