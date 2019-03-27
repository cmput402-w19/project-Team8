# CMPUT 402 Final Project
## Members
#### Matthew Chung, Hiu Fung Kevin Chang, Henry Truong

## Goal:
The question we are addressing is; **'Do number of tests correlate with more merges into production code'**

## Method:
To conduct this experiment, we will be sampling repositories from TravisTorrent and using github mining tools. Our sampling strategy is to select the first 30-50 unique github repositories in the dataset. We will then use PyDriller (maybe) to mine the repositories to discover any patterns and combine it with the attributes of interest from the dataset.

An example of how we might evaluate repositories is detailed below: 

| PR has tests  | Number of added tests | Contributed test coverage | Merge status |
| ------------- | ---------------- | --------------- | ------------- |
|       T       |        3         |        50%      |       T       |
|       F       |        5         |        20%      |       F       |

## Related works:
1. The study conducted discusses the challenges of having stable code before releases and the limited resources available to properly integrate code. This relates to one of our attributes of production ready PRs versus regular PRs.

2. The paper looks into the importance of testing in CI despite the number of build failures resulting from testing. This helps to give insight on test failures and how these failures are combatted over time in the next build. Some ways these failures could be addressed may be an increase in test cases or even fixing a bug caught.

3. This paper outlined how the TravisTorrent dataset is being built. It analyzed builds from GitHub and Travis-CI to synthesis Travis-CI meta data, project data and analysis on build logs.

4. The two main research questions in the paper are: 1: How is the productivity of teams affected by CI 2: What is the effect of CI on software quality. This is similar to our project and can give us insight on what metrics can be used to evaluate software quality for successful release cycles.

## Future insights:
Insights obtained from this project can help determine an effect on number of tests in a build and the number of successful build merges and successful releases. This can give suggestions on best testing methodologies to adopt in order to improve overall releases. 


## References

Holck, J., & Jørgensen, N. (2003). Continuous Integration and Quality Assurance: a case study of two open source projects. Australasian Journal of Information Systems, 11(1). doi:http://dx.doi.org/10.3127/ajis.v11i1.145

Beller, M., Gousios, G., & Zaidman, A. (2016). Oops, my tests broke the build: An analysis of Travis CI builds with GitHub. doi:10.7287/peerj.preprints.1984

Beller, M., Gousios, G., & Zaidman, A. (2017). TravisTorrent: Synthesizing Travis CI and GitHub for Full-Stack Research on Continuous Integration. In 2017 IEEE/ACM 14th International Conference on Mining Software Repositories (MSR). IEEE. https://doi.org/10.1109/msr.2017.24

Vasilescu, B., Yu, Y., Wang, H., Devanbu, P., & Filkov, V. (2015). Quality and productivity outcomes relating to continuous integration in GitHub. In Proceedings of the 2015 10th Joint Meeting on Foundations of Software Engineering - ESEC/FSE 2015. ACM Press. https://doi.org/10.1145/2786805.2786850


## Libraries

### PyDriller

Installation instructions can be found here: https://github.com/ishepard/pydriller#install  
```
pip3 install pydriller
```


### TravisTorrent
Using sqlite3 to query this, download the latest csv from here: https://travistorrent.testroots.org/page_access/

Import to sqlite3 using:  
```
sqlite3 travis.db
.mode csv
.import path/to/travisTorrent.csv travis
```
Now there will be a a table called travis in your new travis.db containing all the data; takes about 5-10 minutes to complete the import.  


