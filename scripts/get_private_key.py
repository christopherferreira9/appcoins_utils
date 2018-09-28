import os
import sys
from eth_account import Account
import json
import getpass

def get_private_key(password: str, f: str) -> Account:
    if not os.path.exists(f):
        print("JSON Keystore not found.")
        sys.exit()

    with open(f, "r") as f:
        data = json.load(f)

    return Account.decrypt(password=password, keyfile_json=data).hex().strip("0x")


if __name__ == "__main__":
    keystore = input("Keystore name (it must exist in the same directory as this script or you must provide a full path to it): ")
    password = getpass.getpass("Password: ")

    print(get_private_key(password=password, f=keystore))
