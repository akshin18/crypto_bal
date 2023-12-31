from web3 import Web3
import json
from db.db_commit import StatiscticCommit
import time










class EtherChecker:
    def __init__(self,node_url="https://eth.llamarpc.com") -> None:
        self.name = "eth"
        self.node_url = node_url
        self.w3 = Web3(Web3.HTTPProvider(self.node_url))
        self.usd_abi = json.loads(open("checker/abis/usd_abi.json","r").read())

        self.usdt_contract_address = Web3.to_checksum_address("0xdac17f958d2ee523a2206206994597c13d831ec7")
        self.usdt_contract = self.w3.eth.contract(address=self.usdt_contract_address, abi=self.usd_abi)

        self.usdc_contract_address = Web3.to_checksum_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
        self.usdc_contract = self.w3.eth.contract(address=self.usdc_contract_address, abi=self.usd_abi)
        self.addresses = {}
        
    
    def add_addresses(self,position,addresses):
        self.addresses.update({position:addresses})
    
    def check_usdt(self,address):
        try:
            ethereum_address = Web3.to_checksum_address(address)
            usdt_balance_wei = self.usdt_contract.functions.balanceOf(ethereum_address).call()
            usdt_balance = self.w3.from_wei(usdt_balance_wei, "mwei")
            return round(usdt_balance,2)
        except:
            return self.check_usdt(address)
    

    def check_usdc(self,address):
        try:
            ethereum_address = Web3.to_checksum_address(address)
            usdc_balance_wei = self.usdc_contract.functions.balanceOf(ethereum_address).call()
            usdc_balance = self.w3.from_wei(usdc_balance_wei, "mwei")
            return round(usdc_balance,2)
        except:
            return self.check_usdc(address)

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
    "0x8F0F8b55083F165D5E819875586B819B3a97905f",
    "0x8d5f663a8806Fe9aCF512600743ABDB99307B98E",
    "0xe159b6Ea834B8aba51f3753955DE44566923a88A",
    "0xfAba6E428FF441cEfC19A9d48d3a69ADcE1c7d5d",

    ]
    ether = EtherChecker()
    for i in addresses:
        print(ether.check_usdt(i),ether.check_usdc(i))

