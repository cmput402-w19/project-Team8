from pydriller import RepositoryMining

''' 
searchSHA: String of the commit hash that you are looking for (this should be a PR)
mergeCommit: Will become the string of the corresponding merge commit for that PR search hash
testList: Array of testfiles that have been modified in this PR
repositoryLink: The https url to the git repository you are mining
'''

searchSHA = 'b7b1c7f11b70d4758a5fe86f507a10e1b8c982eb'
mergeCommit = ''
checkMergeFlag = False
testList = []
repositoryLink = "https://github.com/AChep/AcDisplay.git"

for commit in RepositoryMining(repositoryLink).traverse_commits():
    if (searchSHA in commit.hash):
        checkMergeFlag = True

    if checkMergeFlag is True:
        if commit.merge is True:
            mergeCommit = commit.hash
            for modified_file in commit.modifications:
                if ("Test" in modified_file.filename or "test" in modified_file.filename):
                    testList.append(modified_file.filename)
            break
        
print("The corresponding merge commit hash is " + str(mergeCommit) + " with these possible tests " + str(testList))
