import json
import sys

input_data = json.load(open(sys.argv[1], 'r'))

user = input_data['user']
issue_id = input_data['issue_id']


try:
    data = json.load(open(sys.argv[2], 'r'))
except Exception as e:
    print("Invalid input JSON")
    sys.exit(1)

try:
    global_state = json.load(open('tokens.json', 'r'))
except Exception as e:
    print("Failed to load global state")
    sys.exit(1)


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
        print("Token already deployed")
        sys.exit(1)
    
    global_state[tick] = {
        "p": data['p'],
        "max": data['max'],
        "lim": data['lim'],
        "bal": 0
    }
    print("Deployed " + tick + " token")

    with open("tokens.json", "w") as f:
        json.dump(global_state, f, indent=4)

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
        print("Token not deployed")
        sys.exit(1)

    token = global_state[tick]
    
    # amt check
    amt = int(data['amt'])
    if amt <= 0:
        print("Invalid amount")
        sys.exit(1)

    if amt > int(token['lim']):
        print("Mint amount exceeds limit (limit = " + token['lim'] + ")")
        sys.exit(1)

    if amt + int(token['bal']) > int(token['max']):
        available = int(token['max']) - int(token['bal'])
        print("Mint amount exceeds max supply (available = " + str(available) + ")")
        sys.exit(1)

    # mint
    global_state[tick]['bal'] = int(token['bal']) + amt

    with open("inscriptions/" + issue_id + ".json", "w") as f:
        json.dump({
            "user": user,
            "tick": data["tick"],
            "amt": data["amt"],
            "op": "mint",
            "p": data["p"]
        }, f, indent=4)

    with open("tokens.json", "w") as f:
        json.dump(global_state, f, indent=4)

    print("Minted " + str(amt) + " " + tick + " tokens")