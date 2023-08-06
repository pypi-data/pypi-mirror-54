import unittest
import time
import random
from moneymour.crypto_utils import Signature

from Crypto.PublicKey import RSA

test_private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAvT3czEWmcTH6ITffOJFvvKdsS6iv1A3+OnhmOeZKbdLD+OWe
ivWmXr+6VCNT4qcL+aMfii+W8Hon3DCnqeyab2MY7rIqtwA+xFafTYFHhQU5nsCC
HMWU6LXXX9Jc8xWycK9PGhEkptvIYsgrKzNIXqkp1kM+aX/ZmSqgqjpSODce/FVD
Pt56NWMowoIsppnRSm11NoDPp5o1el5kZSIoRQCTULSFVrl4fdGYKel3JjkfJ1ul
2RhpPz012NY5T09hjYB3J0nIRv6LhisubcB4AFfTj/u8Ivmmlo0txlGKitrUPNXO
YX4+Cpv3myZWwB78LzBwmsz/PTmmqBWalv1MOQIDAQABAoIBAHqcgFihsAubU/L9
3lUqdfkHiPUkYHfGcTe1FpbhDMxHSM4VCDoEmzy8gJ9PHGS30tx1wlOoLeW1X+oc
ZCWGtTECRf8x1NcpA4H2ldSDtLENB55CIIs/wRFd8COXir29CxZTn67F+Ldbo2PN
SZr96R/b/s1iWCfGvFeu9NYWX3snrgpA9WD3DgY0cZo/A3AH1VxvFgeqbg6PzlLs
mee28oLkSYyCsjXnCmCMMjnsP6JZyeC5HCF2wYHNPpnVJFPHO0G0VFge3K6JUGrd
CM5vKGmCLfTdkihK82mdy9rd6i5OFRjEIGj0iD8qUUnoy4Bg13mPSz7FzNKyuwBW
NqKufzkCgYEA52YZy2AfxoIlaDekdhxuYqa+iz4Qq/5oZUhmbZ8dM9yEBtrGc75Z
AK3PZWZ6Hxaudj22Za/E4O0Ndugps4TXRSlqqP6lJ76yZwqBsE3c07tNuoNIJPjN
xBnCDp7gFPgvrEAUSQNyMCwLp+PSlL0B/tyfJzsTqwHhVscBZjf/o3MCgYEA0Vxi
g4S37nl7OWHIAsZwazOH1Om2cCyKnSl5bIpgSp9nuN1oqyLahAqqoS0kpfmQTS+D
xd4LOlPbpu0tvtroHCTnk0P7pMfIMBTle3/JErpACSnDhlhJNg6T1vW0vFbMwMFK
ll/ctTW9DigB1yeP4KWFVRsVnDCj6p+DXCT8XqMCgYBdBdSUx52+hY9YKBY7TQ6r
JfEvtNGq8ukw3jwfEXoB4UJKJyTkXr8U4MqhLuMlIE8eRYzPsCtraKCjDo3FF0Ab
E51HNqdaJPU/KyAbqhF+JKwIsMIN6t99WAWFLyVSCLvReSkueO4so2hEI/gBx0HI
HRT2Bm/PrT/TTMkpOJXSNQKBgQCzmouwxAR+gpzhhy7soowCizx1vOGTrcJkPRY7
tSISIln6z4Zheg73w6bJik6sTEIs1Rw4fNoo+ZOvyjy6RFVm/4niXindHL5x8RtF
LUSz2i/hLIDeGZME2tCdUj/wao5QtgFkq2xN0IIVSOD7UKcvUw/lCM0rJtcYCivI
urn9/QKBgEafuvActDep6KE5iHG1ecVpLiyh4hlEemQsXUwwQwM8m1HmeMbkGZbX
XxEV1nAnFB3KMGgaKQPtNYWN6GRqI0iYQetDJI1bD/GR082l0kX+a4k1LwqazW5G
BV1aiWzsnSB2aNFSZKVPUWFmqtyxxb8d75yyp4wRdjjHiezZcuKk
-----END RSA PRIVATE KEY-----"""


class SignatureFactoryTest(unittest.TestCase):
    @staticmethod
    def test_sign():
        signature = Signature.build(test_private_key, 1572281748, 'body')
        assert signature == b'SfjAYr56Nc6maLSALCdLDxb6X9sPMQ3RBRRzPqEEfsEtpkUTDchE8svBn4ZlWvPRjySZ+lopAuJfoEDMUdmrxVGCXG/tD0DGe1efakDyyVVQPnciuahZtAwVqaz2G/ws8LXCfTkdc/D3Fa/Ts+y+CILcbpbujKXH28BGiQtp/qB4tnvbNVTLKjg2U85Cxx70Oe6A7GPB87vfZx61smYPBq27o+uLYPQ8rnxBdqkgMZH5oZ1NwN0yHDeXGpgt+PljKKFpWTLm1umFidETkM2B8o4HfgvL+gNyjEvUwnCOqjKqHTjqZYKFE1sJVZSdTagBOP7W5p4XoOSebBhBh/YYlA=='

    @staticmethod
    def test_verify():
        rsa_key = RSA.generate(4096)
        public_key = rsa_key.publickey().exportKey("PEM")
        private_key = rsa_key.exportKey("PEM")

        body = {
            'phoneNumber': '+39' + str(random.randrange(1000000000, 9999999999)),
            'orderId': '12345678',
            'amount': 500,
            'products': [
                {
                    'name': 'GoPro Hero7 É',
                    'amount': 500
                }
            ]
        }

        expires_at = time.time()
        signature = Signature.build(private_key, expires_at, body)

        assert Signature.verify(signature, expires_at, body, public_key)
