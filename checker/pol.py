from web3 import Web3
import json
from db.db_commit import StatiscticCommit
import time










class PolygonChecker:
    def __init__(self,node_url="https://polygon.llamarpc.com") -> None:
        self.name = "pol"
        self.node_url = node_url
        self.w3 = Web3(Web3.HTTPProvider(self.node_url))
        self.usd_abi = json.loads(open("checker/abis/usd_abi.json","r").read())

        self.usdt_contract_address = Web3.to_checksum_address("0xc2132D05D31c914a87C6611C10748AEb04B58e8F")
        self.usdt_contract = self.w3.eth.contract(address=self.usdt_contract_address, abi=self.usd_abi)

        self.usdc_contract_address = Web3.to_checksum_address("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
        self.usdc_contract = self.w3.eth.contract(address=self.usdc_contract_address, abi=self.usd_abi)
        self.addresses = {}
        
    
    def add_addresses(self,position,addresses):
        self.addresses.update({position:addresses})
    
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


    def _check_all(self):
        if self.addresses == {}:
            print("go to the rest")
            time.sleep(5)
        else:
            res = all([self.addresses[x] == [] for x in self.addresses])
            if res:
                print("empty now")
                StatiscticCommit.commit()
                return False
            
            for i in self.addresses:
                # print("go addres check")
                if i == 1:
                    try:
                        statistic = self.addresses[i].pop()
                        # print(statistic.address.address,"My address")
                        balance = self.check_usdt(statistic.address.address)
                        # print("balance 1:",balance)
                        StatiscticCommit.update(statistic,balance)
                    except Exception as e:
                        print(e)
                if i == 2:
                    try:
                        statistic = self.addresses[i].pop()
                        # print(statistic.address.address,"My address")
                        balance = self.check_usdc(statistic.address.address)
                        # print("balance 2:",balance)
                        StatiscticCommit.update(statistic,balance)
                    except Exception as e:
                        print(e)
                    
        return True




if __name__ == "__main__":

    addresses =[
    "0xFe14A789E80741c41afd123B8a8FfB88dddb49ae",
    "0x37Db450EaD1AefAd6C38FBEFcA616F8f5c0CFA23",
    "0x53227c83a98Ba1035FEd912Da6cE26a0c11C7C66",

    ]
    ether = PolygonChecker()
    for i in addresses:
        print(ether.check_usdt(i),ether.check_usdc(i))

