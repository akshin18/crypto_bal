from web3 import Web3
import json











class OptimismChecker:
    def __init__(self,node_url="https://optimism.llamarpc.com") -> None:
        self.name = "opt"
        self.node_url = node_url
        self.w3 = Web3(Web3.HTTPProvider(self.node_url))
        self.usd_abi = json.loads(open("abis/usd_abi.json","r").read())

        self.usdt_contract_address = Web3.to_checksum_address("0x94b008aA00579c1307B0EF2c499aD98a8ce58e58")
        self.usdt_contract = self.w3.eth.contract(address=self.usdt_contract_address, abi=self.usd_abi)

        self.usdc_contract_address = Web3.to_checksum_address("0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85")
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
    "0x1111111254EEB25477B68fb85Ed929f73A960582",
    "0x2aB22ac86b25BD448A4D9dC041Bd2384655299c4",

    ]
    ether = OptimismChecker()
    for i in addresses:
        print(ether.check_usdt(i),ether.check_usdc(i))

