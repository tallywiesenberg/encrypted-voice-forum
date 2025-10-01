# user_sign.py
from eth_account import Account
from eth_account.messages import encode_defunct
from dotenv import load_dotenv

# Load private key (⚠️ user should keep this safe)
PRIVATE_KEY = "0xYOUR_PRIVATE_KEY"

# Define the challenge message (must match server)
message = encode_defunct(text="Whitelist Access v1")

# Sign message
acct = Account.from_key(PRIVATE_KEY)
signature = Account.sign_message(message, private_key=PRIVATE_KEY)

print("Ethereum address:", acct.address)
print("Signature:", signature.signature.hex())