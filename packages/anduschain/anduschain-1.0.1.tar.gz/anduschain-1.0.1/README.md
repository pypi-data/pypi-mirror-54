# anduschain-python

## Install

```$xslt
pip install anduscahin
```

## Usage
```$xslt
from web3 import Web3
from anduschain.middleware import construct_sign_and_send_raw_middleware

my_provider = Web3.HTTPProvider('http:/RPC-URL:8545')
w3 = Web3(my_provider)

ADDRESS = '0xfef6f81c2c9e1fa327cad572d352b913bc074a0d'
KEY_FILE = './tmp/UTC--2019-09-30T08:50:41Z--fef6f81c2c9e1fa327cad572d352b913bc074a0d.json'
KEY_PASS = 'KEYPASS

sender = Web3.toChecksumAddress(ADDRESS)

# read local keyfile
with open(KEY_FILE) as keyfile:
    encrypted_key = keyfile.read()
    private_key = w3.eth.account.decrypt(encrypted_key, KEY_PASS)

# add anduschain middleware
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
w3.eth.defaultAccount = sender

try:
    result = w3.eth.sendTransaction({'to': sender, 'gas': 21000, 'value': 1})
    print(Web3.toHex(result))
except Exception as err:
    print("=====Exception======", str(err))
```
