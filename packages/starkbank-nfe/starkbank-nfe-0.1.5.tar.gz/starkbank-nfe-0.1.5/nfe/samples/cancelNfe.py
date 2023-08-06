# -*- coding: utf-8 -*-
from nfe.gateways.saopaulo import SaopauloGateway
from time import sleep

parameters = {
    "CPFCNPJRemetente": "20018183000180",
    "InscricaoPrestador": "57038597",
    "NumeroNFe": "441"
}

# for i in range(409, 441):
#     parameters = {
#         "CPFCNPJRemetente": "20018183000180",
#         "InscricaoPrestador": "57038597",
#         "NumeroNFe": str(i)
#     }

json, status = SaopauloGateway.cancelRps(
    privateKey=open("../static/newRsaKey.pem").read(),
    certificate=open("../static/newCertStark.pem").read(),
    **parameters
)

print(json)
print(status)
sleep(3)
