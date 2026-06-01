from web3 import Web3
import json
import os

SEPOLIA_RPC_URL = os.environ.get("SEPOLIA_RPC_URL")
if SEPOLIA_RPC_URL:
    SEPOLIA_RPC_URL = SEPOLIA_RPC_URL.strip('"\' ')

OWNER_PRIVATE_KEY = os.environ.get("OWNER_PRIVATE_KEY")
if OWNER_PRIVATE_KEY:
    OWNER_PRIVATE_KEY = OWNER_PRIVATE_KEY.strip('"\' ')

if SEPOLIA_RPC_URL:
    w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
    print(f"[INFO] Connecting to Sepolia Network via RPC: {SEPOLIA_RPC_URL}")
else:
    GANACHE_URL = "http://127.0.0.1:7546"
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    print("[INFO] Connecting to Local Ganache")

if not w3.is_connected():
    print("[ERROR] Cannot connect to Ethereum network! Check your provider URL.")
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

deployer = w3.eth.accounts[0] if not OWNER_PRIVATE_KEY else w3.eth.account.from_key(OWNER_PRIVATE_KEY).address
print(f"[DEPLOY] Deploying Attendance contract from address: {deployer}...")

AttendanceContract = w3.eth.contract(abi=abi, bytecode=bytecode)

try:
    if not OWNER_PRIVATE_KEY:
        # Submit local Ganache transaction to deploy
        tx_hash = AttendanceContract.constructor().transact({"from": deployer, "gas": 3000000})
        print("[WAIT] Waiting for transaction receipt...")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    else:
        # Submit signed transaction to Sepolia public net
        print("[BUILD] Building deployment transaction...")
        construct_tx = AttendanceContract.constructor().build_transaction({
            'from': deployer,
            'nonce': w3.eth.get_transaction_count(deployer),
            'gas': 3000000,
            'gasPrice': w3.eth.gas_price,
            'chainId': 11155111 # Sepolia Chain ID
        })
        
        print("[SIGN] Signing transaction with MetaMask Private Key...")
        signed_tx = w3.eth.account.sign_transaction(construct_tx, private_key=OWNER_PRIVATE_KEY)
        
        print("[SEND] Broadcasting raw transaction to Sepolia Testnet...")
        raw_tx = getattr(signed_tx, "raw_transaction", getattr(signed_tx, "rawTransaction", None))
        tx_hash = w3.eth.send_raw_transaction(raw_tx)
        print("[WAIT] Waiting for transaction receipt on Sepolia network...")
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