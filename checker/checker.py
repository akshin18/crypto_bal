from checker.arb import ArbitumChecker
from checker.ava import AvalancheChecker
from checker.bsc import BscChecker
from checker.eth import EtherChecker
from checker.fan import FantomChecker
from checker.opt import OptimismChecker
from checker.pol import PolygonChecker

from threading import Thread as th
import time



class Checker:
    def __init__(self) -> None:
        # self.addresses = addresses
        self.arb_c = ArbitumChecker()
        self.ava_c = AvalancheChecker()
        self.bsc_c = BscChecker()
        self.eth_c = EtherChecker()
        self.fan_c = FantomChecker()
        self.opt_c = OptimismChecker()
        self.pol_c = PolygonChecker()
        self.chains = [self.arb_c,self.ava_c,self.bsc_c,self.eth_c,self.fan_c,self.opt_c,self.pol_c]


    def _check_all(self,chain):
        print("start")
        time.sleep(5)
        while True:
            if chain.addresses != {}:
                # print("start check all",chain.name)
                res = chain._check_all()
                if res == False:
                    break
            else:
                time.sleep(5)
            ...
        print("done")

    def check_all(self):
        for chain in self.chains:
            th(target=self._check_all,args=(chain,)).start()
        