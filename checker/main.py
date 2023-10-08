import time
import threading

from checker import Checker

addresses = [
    "0xFe14A789E80741c41afd123B8a8FfB88dddb49ae",
    "0x1f8642A8Bc400385f6b8888B2568207C38A0BF68",
    "0xfaE2AE0a9f87FD35b5b0E24B47BAC796A7EEfEa1",
    "0xFe14A789E80741c41afd123B8a8FfB88dddb49ae",
    "0xEC4A477501bc22Bbe6aF57dB414d399E800f061e",
    "0x53227c83a98Ba1035FEd912Da6cE26a0c11C7C66",
    "0xFe14A789E80741c41afd123B8a8FfB88dddb49ae",
    "0x5f5d385397095AaED4daffe336F9815AC598DFf5",
    "0xCB99FE720124129520f7a09Ca3CBEF78D58Ed934",
    "0x8d5f663a8806Fe9aCF512600743ABDB99307B98E",
    "0xe159b6Ea834B8aba51f3753955DE44566923a88A",
    "0xfAba6E428FF441cEfC19A9d48d3a69ADcE1c7d5d",
    "0xFe14A789E80741c41afd123B8a8FfB88dddb49ae",
    "0x37Db450EaD1AefAd6C38FBEFcA616F8f5c0CFA23",
    "0x7250eE43718Be514bb45A9B631E963E7b4A23d7E",
    "0x1111111254EEB25477B68fb85Ed929f73A960582",
    "0x2aB22ac86b25BD448A4D9dC041Bd2384655299c4",
    "0x37Db450EaD1AefAd6C38FBEFcA616F8f5c0CFA23",
    "0x53227c83a98Ba1035FEd912Da6cE26a0c11C7C66",
    "0x37Db450EaD1AefAd6C38FBEFcA616F8f5c0CFA23",
    "0x53227c83a98Ba1035FEd912Da6cE26a0c11C7C66",
]

c = Checker(addresses)
t1 = time.time()
c.check_all()
while True:
    if threading.active_count() == 1:
        break
print(time.time()-t1)

networks = [
    "etherium", # +
    "bsc", # +
    "polygon", # +
    "avalanche", # +
    "fantom", # +
    "arbitum", # + 
    "optimism" # +
]