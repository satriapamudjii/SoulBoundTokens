from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_TOKEN = os.getenv('ETHERSCAN_TOKEN')
INFURA_URL = os.getenv('INFURA_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
OWNER_ADDRESS = os.getenv('OWNER_ADDRESS')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
CONTRACT_ABI = os.getenv('CONTRACT_ABI')

web3 = Web3(Web3.HTTPProvider(INFURA_URL))

def deploy_contract():
    compiled_contract_path = 'path_to_compiled_contract'
    deployed_contract_address = web3.eth.contract(
        abi=contract_abi,
        bytecode=contract_bytecode)
    tx_dict = deployed_contract_address.constructor().buildTransaction({
        'from': OWNER_ADDRESS,
        'nonce': web3.eth.get_transaction_count(OWNER_ADDRESS),
        'gasPrice': web3.eth.gas_price,
        'chainId': 3
    })
    signed_tx = web3.eth.account.sign_transaction(tx_dict, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress

def issue_token(to_address):
    contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    nonce = web3.eth.get_transaction_count(OWNER_ADDRESS)
    tx_dict = contract.functions.mint(to_address, 1).buildTransaction({
        'chainId': 3,
        'gas': 70000,
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce,
    })
    signed_tx = web3.eth.account.sign_transaction(tx_dict, PRIVATE_KEY)
    tx_hash = web2.eth.send_raw_transaction(signed_tx.rawTransaction)
    return web3.toHex(tx_hash)

def transfer_token(from_address, to_address):
    contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    nonce = web3.eth.getTransactionCount(from_address)
    tx_dict = contract.functions.transfer(to_address, 1).buildTransaction({
        'chainId': 3,
        'gas': 70000,
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce,
        'from': from_address
    })
    signed_tx = web3.eth.account.sign_transaction(tx_dict, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return web3.toHex(tx_hash)

def verify_ownership(owner_address, token_id):
    contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    return contract.functions.ownerOf(token_id).call() == owner_address