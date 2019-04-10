# CMPUT 402 Final Project Replication Instructions
## Members
#### Matthew Chung, Hiu Fung Kevin Chang, Henry Truong

## Goal:
The question this project aims to address is; 

**'Do number of tests correlate with more merges into production code'**

## Method:
To conduct this experiment, we sample repositories from TravisTorrent and use github mining tools. Our sampling strategy was to find 30 repositories that contain as close as possible to 15 non-merged and 15 merged pull requests in the TravisTorrent data set. We then use the Github API to mine the repositories and compare how test density and assert density look before the PR and after the PR.

## Replication Instructions: 

### Libraries

#### Python3

All of our required libraries for python can be installed using 
```
pip3 install -r requirements.txt
```

#### TravisTorrent
Using sqlite3 to query this, download our csv from here: https://travistorrent.testroots.org/page_access/

This csv can be imported to sqlite3 using:  
```
sqlite3 travis.db
.mode csv
.import path/to/travisTorrent.csv travis
```
Now there will be a a table called travis in your new travis.db containing all the data; takes about 5-10 minutes to complete the import.  

### Instructions 

#### Raw Data
You *must* have the results/test_density_export folder to collect the exported data.

Run
```
python3 findMergeCommit.py
```
This will take several hours to complete, it will generate in the `results/test_density_export` folder a unique csv file for each repository analyzed. This csv file will contain all of the pull request data of interest and will look something like this:

*insert image here*

#### Scatterplots
You *must* have the results/plots folder to collect the exported plots.

Run
```
python3 scatterPlot.py 
```
There are three plots which will be generated in the results/plots folder;

overall_scatter_plot.png: This plot shows all of our data, with Assert Density on the Y-Axis and Test Case Density on the X-Axis. It contains all 861 Pull requests and plots the *difference* in their respective x and y axis values from before the PR and the end of the PR.

focused_overall_scatter_plot.png: This plot is similar to the one above and shows all of our data, with Assert Density on the Y-Axis and Test Case Density on the X-Axis, however it excludes some of the egregious outliers so that we can better see the distribution of data

type3_scatter_plot.png: This plot shows the data for the 10 repositories we found to have *explicit* reference to a contribution policy that referenced tests as being necessary for PRs
