from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

mnemonic_fetch = os.getenv("MNEMONIC")
contract_address = os.getenv("CONTRACT_ADDRESS")

seed_bytes = Bip39SeedGenerator(mnemonic_fetch).Generate()
bip44_def_ctx = Bip44.FromSeed(
    seed_bytes, Bip44Coins.COSMOS).DeriveDefaultPath()

wallet = LocalWallet(PrivateKey(bip44_def_ctx.PrivateKey().Raw().ToBytes()))

ledger = LedgerClient(NetworkConfig.fetch_mainnet())

contract = LedgerContract(None, ledger, address=contract_address)


def update_price():
    res = cg.get_price(ids='fetch-ai', vs_currencies='usd')
    usd_price = res["fetch-ai"]["usd"]
    tx = contract.execute(
        args={
            "admin": {
                "update_price_scheme": {
                    "new_price_scheme": {
                        "price_ranges": [
                            {"min": 3, "max": 3, "price": {
                                "denom": "afet",
                                "amount": str(int(50.0 / usd_price * 10**18))  # "524000000000000000000"
                            }
                            },
                            {"min": 4, "max": 6, "price": {
                                "denom": "afet",
                                "amount": str(int(25.0 / usd_price * 10**18))  #"262000000000000000000"
                            }
                            },
                            {"min": 7, "max": 14, "price": {
                                "denom": "afet",
                                "amount": str(int(10.0 / usd_price * 10**18)) # "105000000000000000000"
                            }
                            }
                        ]

                    }
                }
            }
        },
        sender=wallet
    ).wait_to_complete()
    print(tx.response)


import time

while True:
    print("Updating price")
    try:
        update_price()
    except Exception as e:
        print("Transaction failed with error: {}".format(e))
    print("Sleeping for 5 minutes\n")
    time.sleep(5*60)
    