import hashlib
import requests
import sys
import json


def get_balance(id, chain):
    balance = 0
    actions = []
    for block in chain:
        block_actions = block['transactions']
        for action in block_actions:
            if action['sender'] == id:
                balance -= action['amount']
                actions.append(action)
            elif action['recipient'] == id:
                balance += action['amount']
                actions.append(action)
    return(balance, actions)


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    f.close()

    # gets last block
    r = requests.get(url=node + "/chain")

    # makes value is json and converts it to python dict
    try:
        data = r.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)

    chain = data['chain']
    balance, transactions = get_balance(id, chain)

    print(f'User with id "{id}" has a balance of {balance}')
    print(f'{transactions}')
