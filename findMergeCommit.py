from pydriller import RepositoryMining
import sqlite3
import requests
import json
import csv

''' 
searchSHA: String of the commit hash that you are looking for (this should be a PR)
mergeCommit: Will become the string of the corresponding merge commit for that PR search hash
testList: Array of testfiles that have been modified in this PR
repositoryLink: The https url to the git repository you are mining
'''
github_oauth_token = '0bb120e003a9efee0ca1e502026ea29cebe191ee'

def get_pull_request_info(repo, pr_num):
    try:
        output = {}
        pr_endpoint = "https://api.github.com/repos/{}/pulls/{}/commits".format(repo, pr_num)
        headers={"Authorization":"token " + github_oauth_token}
        response = requests.get(pr_endpoint, headers=headers)
        json_response = response.json()
        # commit before this pr branch off the original branch
        output["parent_commit"] = json_response[0]["parents"][0]["sha"]
        output["oldest_commit_in_pr"] = json_response[0]["sha"]
        output["latest_commit_in_pr"] = json_response[-1]["sha"]

        files_changed = []
        # files_changed_endpoint = "https://api.github.com/repos/{}/pulls/{}/files".format(repo, pr_num)
        # response = requests.get(files_changed_endpoint, headers=headers)
        # for file_obj in response.json():
        #     # does status: added, modified, deleted matter?
        #     files_changed.append(file_obj["filename"])
        
        output["files_changed"] = files_changed
        return output
    except:
        return None

def find_top_unknown_projects(cur):
    query = """
            SELECT gh_project_name, COUNT(distinct gh_pull_req_num) as distPull
            FROM travis 
            WHERE (git_merged_with = 'unknown' OR git_merged_with = '')
            GROUP BY gh_project_name 
            ORDER BY distPull DESC
            LIMIT 100;
            """
    
    results = cur.execute(query)
    repo_lst = list()
    for row in results:
        repo_lst.append(row[0])
    return repo_lst

def test_density_comparison(cur, merge_commit, before_commit, project): 
    
    query = """
                SELECT DISTINCT t1.gh_test_lines_per_kloc, t2.gh_test_lines_per_kloc, t1.gh_test_cases_per_kloc, t2.gh_test_cases_per_kloc,
                t1.gh_asserts_cases_per_kloc, t2.gh_asserts_cases_per_kloc, t1.tr_log_num_tests_run, t2.tr_log_num_tests_run, 
                t1.tr_log_num_tests_ok, t2.tr_log_num_tests_ok, t1.tr_log_num_tests_failed, t2.tr_log_num_tests_failed,
                t2.git_merged_with
                FROM travis t1, travis t2 
                WHERE t1.git_trigger_commit == ? 
                AND t2.git_trigger_commit == ? 
                AND t1.gh_project_name == ?
                AND t2.gh_project_name == ?
                ORDER BY t2.git_merged_with DESC;
                """
    results = cur.execute(query, (before_commit, merge_commit, project, project))
    # for row in results:
    #     print("Project: " + str(project) + " Before Density: " + str(row[0]) + " After Density: " + str(row[1]) + " Difference: " )
    return results

# Queried over all repos with the highest counts of unknown or blank git_merged_with value
# Grabbed the 30 repos that have the highest amount of REAL rejected PRs which was verified using the github API
def get_repo_names():
    # Took out 'spring-projects/spring-data-examples' and 'brightspot' because its actually not helpful, 
    # # added picasso and jedis 
    repos = ['square/picasso', 'xetorthio/jedis', 'Shopify/identity_cache', 'zendesk/samson', 'rspec/rspec-mocks', 'chef/omnibus', 'geoserver/geoserver', 'projectblacklight/blacklight', 'activeadmin/activeadmin', 'heroku/heroku-buildpack-ruby', 'datastax/java-driver', 'querydsl/querydsl', 'HubSpot/Singularity', 'hw-cookbooks/graphite', 'thoughtbot/shoulda-matchers', 'travis-ci/travis-core', 'prawnpdf/prawn', 'opal/opal', 'expertiza/expertiza', 'test-kitchen/test-kitchen', 'owncloud/android', 'rackerlabs/blueflood', 'adhearsion/adhearsion', 'Shopify/liquid', 'jnicklas/capybara', 'MagLev/maglev', 'rspec/rspec-core', 'celluloid/celluloid', 'heroku/heroku', 'sanemat/tachikoma']
    return repos

def get_success_prs(cur, project): 
    query = """SELECT DISTINCT gh_pull_req_num FROM travis WHERE (git_merged_with = 'merge_button' OR git_merged_with = 'commits_in_master') AND gh_is_pr = "TRUE" AND gh_project_name = ? ORDER BY git_merged_with DESC;"""
    merged_results = cur.execute(query, (project,))
    pr_list = []
    for row in merged_results:
        pr_list.append(row[0])
    return pr_list

def get_failed_prs(cur, project): 
    query = """SELECT DISTINCT gh_pull_req_num FROM travis WHERE (git_merged_with = 'unknown' OR git_merged_with = 'fixes_in_commit' OR git_merged_with = '') AND gh_is_pr = "TRUE" AND gh_project_name = ? ORDER BY git_merged_with DESC;"""
    unknown_results = cur.execute(query, (project,))
    pr_list = []
    for row in unknown_results:
        pr_list.append(row[0])
    return pr_list

def special_subtraction(strAfter, strBefore):
    try:
        val = float(strAfter) - float(strBefore)
    except:
        return "NULL"
    return str(val)

def write_repo_result(results):
    result_file = "./results/test_density_export/{}.csv".format(results[0][0].split("/")[-1])
    with open(result_file, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        headers = ["RepoName", "PrNumber", "Before Line Density", "After Line Density", "Line Density Difference", "Before Test Case Density", "After Test Case Density", "Test Case Density Difference", "Assert Test Cases Before", "Assert Test Cases After", "Assert Test Cases Difference", "Before Num Tests Run", "After Num Tests Run", "Num Tests Run Difference", "Before Num Tests Pass", "After Num Tests Pass", "Num Tests Pass Difference", "Before Num Tests Failed", "After Num Tests Failed", "Num Tests Failed Difference", "PR Merged With"]        
        csv_writer.writerow(headers)
        for result_row in results:
            csv_writer.writerow(result_row)
            
def is_merged(repo_name, pr_num):
    headers={"Authorization":"token " + github_oauth_token}
    check_merge_endpoint = "https://api.github.com/repos/{}/pulls/{}/merge".format(repo_name, pr_num)
    response = requests.get(check_merge_endpoint, headers=headers)
    if response.status_code == 204:
        return True
    return False

# return None if not found
def get_commit_before_first_changes_requested(repo, pr_num):
    endpoint = "https://api.github.com/repos/{}/pulls/{}/reviews".format(repo, pr_num)
    github_oauth_token = "0bb120e003a9efee0ca1e502026ea29cebe191ee"
    headers={"Authorization":"token " + github_oauth_token}
    response = requests.get(endpoint, headers=headers)
    
    for review in response.json():
        # print(review)
        if review["state"] == "CHANGES_REQUESTED":
            return review["commit_id"]
    return None

def get_commit_before_review(repo, pr_num):
    endpoint = "https://api.github.com/repos/{}/pulls/{}/comments".format(repo, pr_num)
    github_oauth_token = "0bb120e003a9efee0ca1e502026ea29cebe191ee"
    headers={"Authorization":"token " + github_oauth_token}
    response = requests.get(endpoint, headers=headers)
    try:
        return response.json()[0]["original_commit_id"]   
    except:
        return None

def main():
    con = sqlite3.connect('travis.db')  
    cur = con.cursor()
    repo_names = get_repo_names()
    for repo_name in repo_names:
        writeFlag = False
        # Failed PR Analysis
        repo_failed_prs = get_failed_prs(cur, repo_name)
        print("Failed PRs" + str(repo_failed_prs))

        print("Analyzing: " + repo_name)
        failed_results_array = list()
        failed_count = 0
        for pr in repo_failed_prs:
            failed_count += 1
            print("Looking at PR: " + str(pr) + " Iteration: " + str(failed_count))
            pr_num = int(pr)

            if (is_merged(repo_name, pr_num) == False):
                output = get_pull_request_info(repo_name, pr_num)
                if (output):
                    results = test_density_comparison(cur, output["latest_commit_in_pr"], output["parent_commit"], repo_name)
                    for row in results:
                        print("Failed PR")
                        # Headers:
                        # RepoName, PrNumber, Before Line Density, After Line Density, Difference, Before Case Density, After Case Density, Difference, Assert Cases Before, Assert Cases After, Difference, Before Num Tests Run, After Num Tests Run, Before Num Tests Okay, After Num Tests Okay, Before Num Tests Failed, After Num Tests Failed
                        diff_line = special_subtraction(row[1], row[0])
                        diff_case = special_subtraction(row[3], row[2])
                        diff_assert = special_subtraction(row[5], row[4])
                        diff_tests_run = special_subtraction(row[7], row[6])
                        diff_tests_okay = special_subtraction(row[9], row[8])
                        diff_tests_failed = special_subtraction(row[11], row[10])

                        failed_results_array.append([repo_name, pr_num, str(row[0]), str(row[1]), diff_line, str(row[2]), str(row[3]), diff_case, str(row[4]), str(row[5]), diff_assert, str(row[6]), str(row[7]), diff_tests_run, str(row[8]), str(row[9]), diff_tests_okay, str(row[10]), str(row[11]), diff_tests_failed, "Closed"])
                        # Before Line Density = row[0] After Line Density = row[1] Before Case Density = row[2] After Case Density = row[3]
                        # Asserts Cases Before = row[4] Asserts Cases After = row[5] Before Num Tests Run = row[6] After Num Test Run = row[7]
                        # Num Tests Okay Before = row[8] Num Tests Okay After = row[9] 
                        # Num Tests Failed Before = row[10] Num Tests Failed After = row[11]
                        # Without this break diaspora PR 3402 repeats four times?
                        break
            if len(failed_results_array) >= 15:
                print("Found 15 rejected PRs")
                break

        # Success and Change Request Analysis
        success_results_array = list()
        repo_success_prs = get_success_prs(cur, repo_name)
        print("Success PRs" + str(repo_success_prs))
        print("Analyzing: " + repo_name)
        success_count = 0
        for pr in repo_success_prs:
            success_count += 1
            print("Looking at PR: " + str(pr) + " Iteration: " + str(success_count))
            pr_num = int(pr)
            

            change_req_commit = get_commit_before_first_changes_requested(repo_name, pr_num)
            review_commit = get_commit_before_review(repo_name, pr_num)

            # If there is a change request in this PR
            if (change_req_commit and len(failed_results_array) < 15):
                output = get_pull_request_info(repo_name, pr_num)
                if (output):
                    results = test_density_comparison(cur, output["latest_commit_in_pr"], change_req_commit, repo_name)
                    for row in results:
                        print("Change Request PR")

                        diff_line = special_subtraction(row[1], row[0])
                        diff_case = special_subtraction(row[3], row[2])
                        diff_assert = special_subtraction(row[5], row[4])
                        diff_tests_run = special_subtraction(row[7], row[6])
                        diff_tests_okay = special_subtraction(row[9], row[8])
                        diff_tests_failed = special_subtraction(row[11], row[10])

                        failed_results_array.append([repo_name, pr_num, str(row[0]), str(row[1]), diff_line, str(row[2]), str(row[3]), diff_case, str(row[4]), str(row[5]), diff_assert, str(row[6]), str(row[7]), diff_tests_run, str(row[8]), str(row[9]), diff_tests_okay, str(row[10]), str(row[11]), diff_tests_failed, "Change_Request"])
                        break
            # If there is a review in this PR
            elif (review_commit and len(failed_results_array) < 15):
                output = get_pull_request_info(repo_name, pr_num)
                if (output):
                    results = test_density_comparison(cur, output["latest_commit_in_pr"], review_commit, repo_name)
                    for row in results:
                        print("Review PR")

                        diff_line = special_subtraction(row[1], row[0])
                        diff_case = special_subtraction(row[3], row[2])
                        diff_assert = special_subtraction(row[5], row[4])
                        diff_tests_run = special_subtraction(row[7], row[6])
                        diff_tests_okay = special_subtraction(row[9], row[8])
                        diff_tests_failed = special_subtraction(row[11], row[10])

                        failed_results_array.append([repo_name, pr_num, str(row[0]), str(row[1]), diff_line, str(row[2]), str(row[3]), diff_case, str(row[4]), str(row[5]), diff_assert, str(row[6]), str(row[7]), diff_tests_run, str(row[8]), str(row[9]), diff_tests_okay, str(row[10]), str(row[11]), diff_tests_failed, "Review"])
                        print("Success: ", len(success_results_array))
                        print("Fail: ", len(failed_results_array))
                        break
            # If this is a merged PR with no change requests
            elif (not(change_req_commit) and len(success_results_array) < 15):
                output = get_pull_request_info(repo_name, pr_num)
                if (output):
                    results = test_density_comparison(cur, output["latest_commit_in_pr"], output["parent_commit"], repo_name)
                    for row in results:
                        print("Successful Merged PR")

                        diff_line = special_subtraction(row[1], row[0])
                        diff_case = special_subtraction(row[3], row[2])
                        diff_assert = special_subtraction(row[5], row[4])
                        diff_tests_run = special_subtraction(row[7], row[6])
                        diff_tests_okay = special_subtraction(row[9], row[8])
                        diff_tests_failed = special_subtraction(row[11], row[10])

                        success_results_array.append([repo_name, pr_num, str(row[0]), str(row[1]), diff_line, str(row[2]), str(row[3]), diff_case, str(row[4]), str(row[5]), diff_assert, str(row[6]), str(row[7]), diff_tests_run, str(row[8]), str(row[9]), diff_tests_okay, str(row[10]), str(row[11]), diff_tests_failed, "Merged"])
                        print("Success: ", len(success_results_array))
                        print("Fail: ", len(failed_results_array))
                        break
            if (len(success_results_array) >= 15 and len(failed_results_array) >= 15):
                print("Found 30")
                write_repo_result(success_results_array + failed_results_array)
                writeFlag = True
                break
        # If we check all the data and still dont get 30 total valid PRs, write to file anyways
        if writeFlag == False:
            write_repo_result(success_results_array + failed_results_array)

    return 

if __name__ == "__main__":
    main()