from web3 import Web3
import json











class ArbitumChecker:
    def __init__(self,node_url="https://arbitrum.llamarpc.com") -> None:
        self.name = "arb"
        self.node_url = node_url
        self.w3 = Web3(Web3.HTTPProvider(self.node_url))
        self.usd_abi = json.loads(open("abis/usd_abi.json","r").read())

        self.usdt_contract_address = Web3.to_checksum_address("0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9")
        self.usdt_contract = self.w3.eth.contract(address=self.usdt_contract_address, abi=self.usd_abi)

        self.usdc_contract_address = Web3.to_checksum_address("0xaf88d065e77c8cC2239327C5EDb3A432268e5831")
        self.usdc_contract = self.w3.eth.contract(address=self.usdc_contract_address, abi=self.usd_abi)
        
    
    def check_usdt(self,address):
        ethereum_address = Web3.to_checksum_address(address)
        usdt_balance_wei = self.usdt_contract.functions.balanceOf(ethereum_address).call()
        usdt_balance = self.w3.from_wei(usdt_balance_wei, "mwei")
        return round(usdt_balance,2)
    

    def check_usdc(self,address):
        ethereum_address = Web3.to_checksum_address(address)
        usdc_balance_wei = self.usdc_contract.functions.balanceOf(ethereum_address).call()
        usdc_balance = self.w3.from_wei(usdc_balance_wei, "mwei")
        return round(usdc_balance,2)


    def _check_all(self,address):
        data = {
            "usdt":self.check_usdt(address),
            "usdc":self.check_usdc(address),
        }
        return data




if __name__ == "__main__":

    addresses =[
    "0xFe14A789E80741c41afd123B8a8FfB88dddb49ae",
    "0x1f8642A8Bc400385f6b8888B2568207C38A0BF68",
    "0xfaE2AE0a9f87FD35b5b0E24B47BAC796A7EEfEa1",

    ]
    ether = ArbitumChecker()
    for i in addresses:
        print(ether.check_usdt(i),ether.check_usdc(i))

