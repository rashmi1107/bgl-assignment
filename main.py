from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from flask import Flask, request
import yaml
import json
import requests

app = Flask(__name__)

def init():
    with open("config.yml", "r") as fptr:
        configDict = yaml.load(fptr, Loader=yaml.FullLoader)
        print("Config read successful")
    return configDict

def check_balance(addressFrom, value):
    balance = web3.eth.get_balance(addressFrom)
    print("Balance: {} - {}".format(balance, value, balance > web3.toWei(1, 'ether')))
    return (balance > web3.toWei(1, 'ether'))

def balance_transfer(addressFrom, addressTo, value, key):
    # print(web3.eth.getTransactionCount(addressFrom))
    # print(web3.eth.getTransactionCount(addressTo))
    signed_txn = web3.eth.account.signTransaction(dict(
        nonce=web3.eth.getTransactionCount(addressFrom),
        gasPrice=web3.eth.gasPrice,
        gas=100000,
        to=addressTo,
        value=value
    ),key)
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(txn_hash)
    if tx_receipt['status'] == 1:
        return "Transfer completed successfully"
    else:
        return "Transfer failed"

def transfer_ether(address1, address2, transfer_amount):
    isFromBalanceSufficient = check_balance(address1, transfer_amount)
    isToBalanceSufficient = check_balance(address2, transfer_amount)
    if isFromBalanceSufficient:
        print("1 -> 2")
        return balance_transfer(address1, address2, transfer_amount, configDict['key1']) + ' from ' + address1 + ' to ' + address2
    elif isToBalanceSufficient:
        print("2 -> 1")
        return balance_transfer(address2, address1, transfer_amount, configDict['key2']) + ' from ' + address2 + ' to ' + address1
    else:
        return "Balance insufficient"

def fetch_balance_and_transact_eth(address1, address2, transfer_amount):
    isFromBalanceSufficient = check_balance(address1, transfer_amount)
    if isFromBalanceSufficient:
        print("1 -> 2")
        return balance_transfer(address1, address2, transfer_amount, configDict['key1']) + ' from ' + address1 + ' to ' + address2
    else:
        return "Balance insufficient"

def approve_transaction(contract, sender, receiver, amount):
    approve = contract.functions.approve(receiver, amount).buildTransaction({'from': sender, 'chainId': 3, 'gas':100000,'nonce': web3.eth.getTransactionCount(sender)})
    # print(approve)
    signed_txn = web3.eth.account.signTransaction(approve, configDict['key1'])
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    # print (txn_hash)
    tx_receipt = web3.eth.waitForTransactionReceipt(txn_hash)
    print(tx_receipt)

def transfer_mytoken(contract, sender, receiver, amount):
    transaction = contract.functions.transferFrom(sender, receiver, amount).buildTransaction({'chainId': 3, 'gas':100000,'nonce': web3.eth.getTransactionCount(sender)})
    # print(transaction);
    signed_txn = web3.eth.account.signTransaction(transaction, configDict['key1'])
    # print(signed_txn)
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    # print(txn_hash)
    tx_receipt = web3.eth.waitForTransactionReceipt(txn_hash)
    # print(tx_receipt)
    if tx_receipt['status'] == 1:
        return "Transfer completed successfully"
    else:
        return "Transfer failed"

def fetch_transaction_report(address):
    requestURL = configDict['etherscan_URL']+address+ "&apikey=" +configDict['etherscan_API_key']
    agent = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
    response = requests.get(requestURL, headers=agent)
    print(response)
    if response.status_code != 200:
        return "Failed to get report of address : " + address
    report = response.json()
    status = report.get("status")
    print(status)
    if status == "1":
        del report['status']
        del report['message']
        return report
    else:
        return "Failed to get report of address : " + address

@app.route('/transact/etherFromAny', methods = ['POST'])
def transact_etherFromAny():
    return transfer_ether(address1, address2, transfer_amount)

@app.route('/transact/ether', methods = ['POST'])
def transact_ether():
    return fetch_balance_and_transact_eth(address1, address2, transfer_amount)

@app.route('/transact/myTKN', methods = ['POST'])
def transact_myTKN():
    # approve_transaction(contract, address1, address2, transfer_amount)
    # exit(0)
    contractAddress = web3.toChecksumAddress(configDict['contract_info']['custom_token_address'])
    contract = web3.eth.contract(address=contractAddress, abi=json.loads(configDict['contract_info']['abi']))
    return transfer_mytoken(contract, address1, address2, transfer_amount)  + ' from ' + address1 + ' to ' + address2

@app.route('/viewReportJSON/<address>', methods = ['GET'])
def view_report(address = None):
    if address:
        return fetch_transaction_report(address)
    return fetch_transaction_report(address1)

if __name__ == "__main__":
    configDict = init()
    web3 = Web3(Web3.HTTPProvider(configDict['infura_URL']))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print("isConnected", web3.isConnected())

    address1 = configDict['address1']
    address2 = configDict['address2']

    transfer_amount = web3.toWei(1, 'ether')
    # transfer_amount = 0*100

    app.run(host="0.0.0.0", port=5000)