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



def get_pull_request_info(repo, pr_num):
    output = {}
    pr_endpoint = "https://api.github.com/repos/{}/pulls/{}/commits".format(repo, pr_num)
    response = requests.get(pr_endpoint)
    json_response = response.json()
    # commit before this pr branch off the original branch
    output["parent_commit"] = json_response[0]["parents"][0]["sha"]
    output["oldest_commit_in_pr"] = json_response[0]["sha"]
    output["latest_commit_in_pr"] = json_response[-1]["sha"]

    files_changed_endpoint = "https://api.github.com/repos/{}/pulls/{}/files".format(repo, pr_num)
    files_changed = []
    response = requests.get(files_changed_endpoint)
    for file_obj in response.json():
        # does status: added, modified, deleted matter?
        files_changed.append(file_obj["filename"])
    
    output["files_changed"] = files_changed
    return output

def test_density_comparison(cur, merge_commit, before_commit, project): 
    
    query = """
                SELECT DISTINCT t1.gh_test_lines_per_kloc as BeforeLineDensity, t2.gh_test_lines_per_kloc as AfterTestDensity 
                FROM travis t1, travis t2 
                WHERE t1.git_trigger_commit == ? 
                AND t2.git_trigger_commit == ? 
                AND t1.gh_project_name == ?
                AND t2.gh_project_name == ?;
                """
    results = cur.execute(query, (before_commit, merge_commit, project, project))
    for row in results:
        print("Project: " + str(project) + " Before Density: " + str(row[0]) + " After Density: " + str(row[1]) + " Difference: " + str(float(row[1]) - float(row[0])))

def get_repo_names(cur):
    query = """select distinct  gh_project_name from travis where (gh_is_pr == "TRUE") LIMIT 30;"""
    results = cur.execute(query)
    repos = []
    for row in results:
        repos.append(row[0])
        #print(row[0])
    return repos

def get_prs(cur, project): 
    query = """select distinct gh_pull_req_num from travis where gh_is_pr == "TRUE" and gh_project_name == ? LIMIT 30;"""
    results = cur.execute(query, (project,))
    pr_list = []
    for row in results:
        pr_list.append(row[0])
    return pr_list

def main():
    con = sqlite3.connect('travis.db')  
    cur = con.cursor()
    repo_names = get_repo_names(cur)
    for repo_name in repo_names:
        repo_prs = get_prs(cur, repo_name)
        print("Analyzing: " + repo_name)
        for pr in repo_prs:
            print("Looking at PR: " + str(pr))
            pr_num = int(pr)
            output = get_pull_request_info(repo_name, pr_num)
            test_density_comparison(cur, output["latest_commit_in_pr"], output["parent_commit"], repo_name)
        # When we are confident that our oauth is setup we can remove this break. Leaving it so we dont get banned
        break
        pass
    return 

if __name__ == "__main__":
    main()