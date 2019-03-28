from pydriller import RepositoryMining
import sqlite3
import requests
import json

''' 
searchSHA: String of the commit hash that you are looking for (this should be a PR)
mergeCommit: Will become the string of the corresponding merge commit for that PR search hash
testList: Array of testfiles that have been modified in this PR
repositoryLink: The https url to the git repository you are mining
'''

# searchSHA = 'b7b1c7f11b70d4758a5fe86f507a10e1b8c982eb'
# mergeCommit = ''
# checkMergeFlag = False
# testList = []
# repositoryLink = "https://github.com/AChep/AcDisplay.git"

# for commit in RepositoryMining(repositoryLink).traverse_commits():
#     if (searchSHA in commit.hash):
#         checkMergeFlag = True

#     if checkMergeFlag is True:
#         if commit.merge is True:
#             mergeCommit = commit.hash
#             for modified_file in commit.modifications:
#                 if ("Test" in modified_file.filename or "test" in modified_file.filename):
#                     testList.append(modified_file.filename)
#             break
        
# print("The corresponding merge commit hash is " + str(mergeCommit) + " with these possible tests " + str(testList))

def get_pull_request_info(repo, pr_num):
    output = {}
    pr_endpoint = "https://api.github.com/repos/{}/pulls/{}/commits".format(repo, pr_num)
    response = requests.get(pr_endpoint)
    json_response = response.json()
    # commit before this pr branch off the original branch
    output["parent_commit"] = json_response[0]["parents"][0]["sha"]
    output["oldest_commit_in_pr"] = json_response[0]["sha"]
    output["latestest_commit_in_pr"] = json_response[-1]["sha"]

    files_changed_endpoint = "https://api.github.com/repos/{}/pulls/{}/files".format(repo, pr_num)
    files_changed = []
    response = requests.get(files_changed_endpoint)
    for file_obj in response.json():
        # does status: added, modified, deleted matter?
        files_changed.append(file_obj["filename"])
    
    output["files_changed"] = files_changed
    return output


def get_repo_names(cur):
    query = """select distinct  gh_project_name from travis where (gh_is_pr == "TRUE") LIMIT 30;"""
    results = cur.execute(query)
    repos = []
    for row in results:
        repos.append(row[0])
        print(row[0])
    return repos

def main():
    con = sqlite3.connect('travis.db')  
    cur = con.cursor()
    repo_names = get_repo_names(cur)
    for repo_name in repo_names:
        # output = get_pull_request_info(repo_name, 202)
        # print(output)
        # break
        pass


    return 

if __name__ == "__main__":
    main()