import requests
import json
import os
import time


token = os.environ.get("GITHUB_TOKEN")

def get_issues(owner, repo, until=None):
    issues = []
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "User-Agent": "PR-Commenter",
        "Accept": "application/vnd.github.v3+json",
    }
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(response.text)
            raise Exception("Error: API request unsuccessful.")
        data = response.json()
        if not data:
            break
        stop = False
        for issue in data:
            if until and issue['number'] <= until:
                stop = True
                break
            issues.append(issue)
        
        if stop:
            break

        if 'next' in response.links.keys():
            url = response.links['next']['url']
        else:
            break
    return issues


def post_comment_to_pr(owner, repo, pr_number, message):
    return
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "User-Agent": "PR-Commenter",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"body": message}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print("Successfully posted the comment!")
    else:
        print(f"Failed to post comment. Status code: {response.status_code}, Response: {response.text}")
    time.sleep(0.5)


def process(issue_id, user, data):
    with open("tokens.json", "r") as f:
        global_state = json.load(f)

    op = data['op']
    # deploy a token
    # {
    #  "p": "GRC20",
    #  "op": "deploy",
    #  "tick": "GitHub",
    #  "max": "1000000000",
    #  "lim": "2000"
    # }

    if op == "deploy":
        # tick check
        tick = data['tick']
        if tick in global_state:
            return {
                "status": "error",
                "message": "Token already deployed"
            }
        
        global_state[tick] = {
            "p": data['p'],
            "max": data['max'],
            "lim": data['lim'],
            "bal": 0
        }

        with open("tokens.json", "w") as f:
            json.dump(global_state, f, indent=4)

        return {
            "status": "success",
            "message": "Deployed " + tick + " token"
        }

    # mint a token
    # {  
    #   "p": "GRC20", 
    #   "op": "mint", 
    #   "tick": "GitHub", 
    #   "amt": "2000"
    # }
    elif op == "mint":
        # tick check
        tick = data['tick']
        if tick not in global_state:
            return {
                "status": "error",
                "message": "Token not deployed"
            }

        token = global_state[tick]
        
        # amt check
        amt = int(data['amt'])
        if amt <= 0:
            return {
                "status": "error",
                "message": "Invalid amount"
            }

        if amt > int(token['lim']):
            print("Mint amount exceeds limit (limit = " + token['lim'] + ")")
            return {
                "status": "error",
                "message": "Mint amount exceeds limit (limit = " + token['lim'] + ")"
            }

        if amt + int(token['bal']) > int(token['max']):
            available = int(token['max']) - int(token['bal'])
            return {
                "status": "error",
                "message": "Mint amount exceeds limit (available = " + str(available) + ")"
            }

        # mint
        global_state[tick]['bal'] = int(token['bal']) + amt

        with open("inscriptions/" + str(issue_id) + ".json", "w") as f:
            json.dump({
                "user": user,
                "tick": data["tick"],
                "amt": data["amt"],
                "op": "mint",
                "p": data["p"]
            }, f, indent=4)

        with open("tokens.json", "w") as f:
            json.dump(global_state, f, indent=4)

        return {
            "status": "success",
            "message": "Minted " + str(amt) + " " + str(tick) + " tokens, inscription at https://github.com/ghscr/ghscription/blob/main/inscriptions/" + str(issue_id) + ".json"
        }


def main():
    owner = "ghscr"  # Replace with the owner of the repo
    repo = "ghscription"    # Replace with the repository name

    last_issue = 0

    if os.path.exists("last_issue.txt"):
        with open("last_issue.txt", "r") as f:
            last_issue = int(f.read())

    issues = get_issues(owner, repo, until=last_issue)
    issues.reverse()
    for issue in issues:
        print(f"Issue #{issue['number']}: {issue['body']} - {issue['user']['login']}")

        try: 
            json.loads(issue['body'])
        except:
            print("Invalid JSON")
            post_comment_to_pr(owner, repo, issue['number'], "Invalid JSON")
            continue
        
        try:
            result = process(issue['number'], issue['user']['login'], json.loads(issue['body']))

            if result['status'] == "success":
                post_comment_to_pr(owner, repo, issue['number'], result['message'])
            else:
                post_comment_to_pr(owner, repo, issue['number'], "Error: " + result['message'])
        except Exception as e:
            post_comment_to_pr(owner, repo, issue['number'], "Something went wrong while processing the inscription. Please check the JSON and try again.")
            print(e)
            continue
        
        with open("last_issue.txt", "w") as f:
            f.write(str(issue['number']))


if __name__ == "__main__":
    main()
