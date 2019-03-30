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
    github_oauth_token = "0bb120e003a9efee0ca1e502026ea29cebe191ee"
    headers={"Authorization":"token " + github_oauth_token}
    response = requests.get(pr_endpoint, headers=headers)
    json_response = response.json()
    # commit before this pr branch off the original branch
    output["parent_commit"] = json_response[0]["parents"][0]["sha"]
    output["oldest_commit_in_pr"] = json_response[0]["sha"]
    output["latest_commit_in_pr"] = json_response[-1]["sha"]

    files_changed_endpoint = "https://api.github.com/repos/{}/pulls/{}/files".format(repo, pr_num)
    files_changed = []
    response = requests.get(files_changed_endpoint, headers=headers)
    for file_obj in response.json():
        # does status: added, modified, deleted matter?
        files_changed.append(file_obj["filename"])
    
    output["files_changed"] = files_changed
    return output

def test_density_comparison(cur, merge_commit, before_commit, project): 
    
    query = """
                SELECT DISTINCT t1.gh_test_lines_per_kloc, t2.gh_test_lines_per_kloc, t1.gh_test_cases_per_kloc, t2.gh_test_cases_per_kloc,
                t1.gh_asserts_cases_per_kloc, t2.gh_asserts_cases_per_kloc, t1.tr_log_num_tests_run, t2.tr_log_num_tests_run, 
                t1.tr_log_num_tests_ok, t2.tr_log_num_tests_ok, t1.tr_log_num_tests_failed, t2.tr_log_num_tests_failed
                FROM travis t1, travis t2 
                WHERE t1.git_trigger_commit == ? 
                AND t2.git_trigger_commit == ? 
                AND t1.gh_project_name == ?
                AND t2.gh_project_name == ?;
                """
    results = cur.execute(query, (before_commit, merge_commit, project, project))
    # for row in results:
    #     print("Project: " + str(project) + " Before Density: " + str(row[0]) + " After Density: " + str(row[1]) + " Difference: " )
    return results

def get_repo_names(cur):
    query = """select distinct  gh_project_name from travis where (gh_is_pr == "TRUE") LIMIT 100;"""
    results = cur.execute(query)
    repos = []
    for row in results:
        repos.append(row[0])
        #print(row[0])
    return repos

def get_prs(cur, project): 
    query = """select distinct gh_pull_req_num from travis where gh_is_pr == "TRUE" and gh_project_name == ? LIMIT 100;"""
    results = cur.execute(query, (project,))
    pr_list = []
    for row in results:
        pr_list.append(row[0])
    return pr_list

def special_subtraction(strAfter, strBefore):
    try:
        val = float(strAfter) - float(strBefore)
    except:
        return "NULL"
    return str(val)

def main():
    con = sqlite3.connect('travis.db')  
    cur = con.cursor()
    repo_names = get_repo_names(cur)
    for repo_name in repo_names:
        repo_prs = get_prs(cur, repo_name)
        print("Analyzing: " + repo_name)
        results_array = list()
        count = 0
        for pr in repo_prs:
            count += 1
            print("Looking at PR: " + str(pr) + " Iteration: " + str(count))
            pr_num = int(pr)
            output = get_pull_request_info(repo_name, pr_num)
            results = test_density_comparison(cur, output["latest_commit_in_pr"], output["parent_commit"], repo_name)
            for row in results:
                # Headers:
                #  RepoName, PrNumber, Before Line Density, After Line Density, Difference, Before Case Density, After Case Density, Difference, Assert Cases Before, Assert Cases After, Difference, Before Num Tests Run, After Num Tests Run, Before Num Tests Okay, After Num Tests Okay, Before Num Tests Failed, After Num Tests Failed
                diff_line = special_subtraction(row[1], row[0])
                diff_case = special_subtraction(row[3], row[2])
                diff_assert = special_subtraction(row[5], row[4])
                diff_tests_run = special_subtraction(row[7], row[6])
                diff_tests_okay = special_subtraction(row[9], row[8])
                diff_tests_failed = special_subtraction(row[11], row[10])

                results_array.append([repo_name, pr_num, str(row[0]), str(row[1]), diff_line, str(row[2]), str(row[3]), diff_case, str(row[4]), str(row[5]), diff_assert, str(row[6]), str(row[7]), diff_tests_run, str(row[8]), str(row[9]), diff_tests_okay, str(row[10]), str(row[11]), diff_tests_failed])
                # Before Line Density = row[0] After Line Density = row[1] Before Case Density = row[2] After Case Density = row[3]
                # Asserts Cases Before = row[4] Asserts Cases After = row[5] Before Num Tests Run = row[6] After Num Test Run = row[7]
                # Num Tests Okay Before = row[8] Num Tests Okay After = row[9] 
                # Num Tests Failed Before = row[10] Num Tests Failed After = row[11]
                # Without this break diaspora PR 3402 repeats four times?
                break
            if len(results_array) >= 30:
                print(results_array)
                break
        break
        pass
    return 

if __name__ == "__main__":
    main()