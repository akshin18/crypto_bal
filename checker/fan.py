from web3 import Web3
import json



# not ready 







class FantomChecker:
    def __init__(self,node_url="https://rpcapi.fantom.network") -> None:
        self.name = "fan"
        self.node_url = node_url
        self.w3 = Web3(Web3.HTTPProvider(self.node_url))
        self.usd_abi = json.loads(open("abis/usd_abi.json","r").read())

        self.tusd_contract_address = Web3.to_checksum_address("0x9879aBDea01a879644185341F7aF7d8343556B7a")
        self.tusd_contract = self.w3.eth.contract(address=self.tusd_contract_address, abi=self.usd_abi)

    
    def check_tusd(self,address):
        ethereum_address = Web3.to_checksum_address(address)
        usdt_balance_wei = self.tusd_contract.functions.balanceOf(ethereum_address).call()
        usdt_balance = self.w3.from_wei(usdt_balance_wei, "ether")
        return round(usdt_balance,2)
    

    def _check_all(self,address):
        data = {
            "tusd":self.check_tusd(address),

        }
        return data






if __name__ == "__main__":

    addresses =[
    "0xFe14A789E80741c41afd123B8a8FfB88dddb49ae",
    "0x37Db450EaD1AefAd6C38FBEFcA616F8f5c0CFA23",
    "0x7250eE43718Be514bb45A9B631E963E7b4A23d7E",

    ]
    ether = FantomChecker()
    for i in addresses:
        print(ether.check_tusd(i))

