from web3 import Web3
import json
import os

GANACHE_URL = "http://127.0.0.1:7546"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if not w3.is_connected():
    print("[ERROR] Cannot connect to Ganache! Make sure Ganache is running on http://127.0.0.1:7546")
    exit(1)

# Paths
BUILD_FILE = os.path.join("..", "blockchain", "build", "contracts", "Attendance.json")
ABI_FILE = "contract_abi.json"

if not os.path.exists(BUILD_FILE):
    print(f"[ERROR] Truffle build not found at {BUILD_FILE}! Run 'npx truffle compile' first.")
    exit(1)

print("[INFO] Loading compiled contract build...")
with open(BUILD_FILE, "r") as f:
    build_data = json.load(f)

abi = build_data["abi"]
bytecode = build_data["bytecode"]

deployer = w3.eth.accounts[0]
print(f"[DEPLOY] Deploying Attendance contract from address: {deployer}...")

AttendanceContract = w3.eth.contract(abi=abi, bytecode=bytecode)

try:
    # Submit transaction to deploy
    tx_hash = AttendanceContract.constructor().transact({"from": deployer, "gas": 3000000})
    print("[WAIT] Waiting for transaction receipt...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress
    print(f"[SUCCESS] Contract successfully deployed!")
    print(f"   Address: {contract_address}")

    # Write to contract_abi.json
    output_data = {
        "address": contract_address,
        "abi": abi
    }

    with open(ABI_FILE, "w") as f:
        json.dump(output_data, f, indent=4)

    print(f"[SAVE] Updated {ABI_FILE} with the deployed address and ABI!")
except Exception as e:
    print(f"[ERROR] Deployment failed: {e}")