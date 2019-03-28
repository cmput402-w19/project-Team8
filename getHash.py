import requests
import json
# endpoint = "https://api.github.com/repos/lardawge/carrierwave_backgrounder/pulls/202/commits"
https://api.github.com/repos/htruong1/dummyRepo/pulls/1/commits
endpoint = "https://api.github.com/repos/forgeno/CMPUT404-group-project/pulls/167/commits"
print(endpoint)
response = requests.get(endpoint)
# responseObj = response.json()[0]["commit"]
responseObj = response.json()
for i in responseObj:
    print(i)
    print()
# for key in responseObj.keys():
#     print(key, responseObj[key])
# for key in response.json()[0].keys():
#     print(key)

# fore every pull request, get the files changed
# get list of files names that the PR changed
# also the commits
# the response.json()[0]["parents"]["sha"] of the response is where you branched off of origianlly
#"0f75d61c3453939caa108a13e1700d03ef2adac1 is wehre we branchd off from (where master pushed to and somethign else)
# [0] is teh oldest commit