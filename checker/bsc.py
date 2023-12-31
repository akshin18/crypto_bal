from web3 import Web3
import json
from db.db_commit import StatiscticCommit
import time










class BscChecker:
    def __init__(self,node_url="https://binance.llamarpc.com") -> None:
        self.name = "bsc"
        self.node_url = node_url
        self.w3 = Web3(Web3.HTTPProvider(self.node_url))
        self.usd_abi = json.loads(open("checker/abis/usd_abi.json","r").read())

        self.busd_contract_address = Web3.to_checksum_address("0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56")
        self.busd_contract = self.w3.eth.contract(address=self.busd_contract_address, abi=self.usd_abi)

        self.usdc_contract_address = Web3.to_checksum_address("0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d")
        self.usdc_contract = self.w3.eth.contract(address=self.usdc_contract_address, abi=self.usd_abi)
        self.addresses = {}
        
    
    def add_addresses(self,position,addresses):
        self.addresses.update({position:addresses})
    
    def check_busd(self,address):
        ethereum_address = Web3.to_checksum_address(address)
        usdt_balance_wei = self.busd_contract.functions.balanceOf(ethereum_address).call()
        usdt_balance = self.w3.from_wei(usdt_balance_wei, "ether")
        return round(usdt_balance,2)
    

    def check_usdc(self,address):
        ethereum_address = Web3.to_checksum_address(address)
        usdc_balance_wei = self.usdc_contract.functions.balanceOf(ethereum_address).call()
        usdc_balance = self.w3.from_wei(usdc_balance_wei, "ether")
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
                        balance = self.check_busd(statistic.address.address)
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
    "0x5f5d385397095AaED4daffe336F9815AC598DFf5",
    "0xCB99FE720124129520f7a09Ca3CBEF78D58Ed934"
    ]
    ether = BscChecker()
    for i in addresses:
        print(ether.check_busd(i),ether.check_usdc(i))

