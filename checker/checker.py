from arb import ArbitumChecker
from ava import AvalancheChecker
from bsc import BscChecker
from eth import EtherChecker
from fan import FantomChecker
from opt import OptimismChecker
from pol import PolygonChecker

from threading import Thread as th




class Checker:
    def __init__(self,addresses:list) -> None:
        self.addresses = addresses
        self.arb_c = ArbitumChecker()
        self.ava_c = AvalancheChecker()
        self.bsc_c = BscChecker()
        self.eth_c = EtherChecker()
        self.fan_c = FantomChecker()
        self.opt_c = OptimismChecker()
        self.pol_c = PolygonChecker()
        self.chains = [self.arb_c,self.ava_c,self.bsc_c,self.eth_c,self.fan_c,self.opt_c,self.pol_c]


    def _check_all(self,chain):
        for address in self.addresses:
            print(chain._check_all(address))

    def check_all(self):
        for chain in self.chains:
            th(target=self._check_all,args=(chain,)).start()
        