import json
import argparse

from web3 import Web3, HTTPProvider

# Example
# python3 approve.py -network ropsten -account_addr <ACCOUNT_ADDR> -account_privkey <PRIVATE_KEY> -amount 0 -allowance_addr <ALLOWANCE_ADDR>

def main(network, account_addr, account_privkey, amount, allowance_addr):
    # Create connection to provider
    w3_obj = Web3(HTTPProvider("https://{}.infura.io/M4rislvVtGFndjSAoNhg".format(network)))
    contract_addr = "0x1a7a8BD9106F2B8D977E08582DC7d24c723ab0DB" if network == "mainnet" else "0xab949343E6C369C6B17C7ae302c1dEbD4B7B61c3"
    
    # Create instance of the smart contract deployed
    abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_value","type":"uint256"}],"name":"burn","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_value","type":"uint256"}],"name":"burnFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Burn","type":"event"}]')
    instance = w3_obj.eth.contract(address=contract_addr,
                                   abi=abi)

    chain_id = 1 if network == "mainnet" else 3
    transact = {'from': account_addr,
                'chainId': chain_id,
                'value': 0x0,
                'gas': 250000,
                'gasPrice': w3_obj.eth.gasPrice * 15,
                'nonce': w3_obj.eth.getTransactionCount(account_addr)}
    tx_raw = instance.functions.approve(allowance_addr, Web3.toWei(amount, "ether")).buildTransaction(transact)
    signed_tx = w3_obj.eth.account.signTransaction(tx_raw, account_privkey)
    txid = w3_obj.eth.sendRawTransaction(signed_tx.rawTransaction)

    print("TX ID   --> {}".format(txid.hex()))
    print("https://{is_ropsten}etherscan.io/tx/{tx}".format(is_ropsten="ropsten." if chain_id == 3 else "", tx=txid.hex()))



if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-network", type=str, choices=["mainnet", "ropsten"])
    PARSER.add_argument("-account_addr", type=str, help="Account approving the allowance")
    PARSER.add_argument("-account_privkey", type=str, help="Private key of the account approving the allowance")
    PARSER.add_argument("-amount", type=str, help="Amount of allowance")
    PARSER.add_argument("-allowance_addr", type=str, help="Account to give the allowance to")
    ARGS = PARSER.parse_args()

    main(ARGS.network,
         Web3.toChecksumAddress(ARGS.account_addr),
         ARGS.account_privkey,
         ARGS.amount,
         Web3.toChecksumAddress(ARGS.allowance_addr))
