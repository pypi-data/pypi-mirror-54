import base64
import json
from datetime import datetime
from datetime import timedelta
from moneymour import environments

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

MONEYMOUR_PUBLIC_KEY_DEVELOPMENT = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0xjRECYz5oKWyjmCOQc3
x9D9eC8v79iRsMScCu9fHesM0Znkto73tvfUhGDmTms6NIgVDDWzLwf40rRPFkxK
zuw0ZGRJDSRw7dGNQ/yjM+R3WOE9HAaUjtX6rX6t/urvQW0XN057/clfMeebEQR0
knJhOuukrgaZC54XbMitlGNk4UxXkbaTD+h0UoSAqxVSM1riUTbNef6mWWHOZGB+
Dpi6lNI6Y6WX9w4nTwXiOWkthM+jsGTV1Vz49UB8gDmcZSgBp1dRLVzTm7NH8H3v
rgrjADr43io1gUC1N0zrXxzyX+xNLABkLW+Oi3lbSXSFFxCjdl2vlUs2SSW78EMD
KwIDAQAB
-----END PUBLIC KEY-----"""

MONEYMOUR_PUBLIC_KEY_STAGE = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAty+wRd3ArC2RfUA1Ypua
KkXp/bEs6KgRX68NrenZ3yk3jx7M72EeQS0tgNvWVfVC3NdhX9rJCM2JgkmlDIOk
keRj+S2BWJ1sIo5a/Haxkgm745Vd1McOz+VciWPY5p9OJB7xQX+sKhrfKzjfWLAs
+e3Kre/l5OzhvzHf7yvzJueRHHvqX9epygVBhaYwiS+VtUhNPmBB0CwTkAUMTIQ1
u2iv0c/beutBHshexO51AzGsH/LHy5LyJcgZYQ3YYRc/KABJb6A02I/V7H1Aa8Uz
qKrx4ZKW1h7t8q3gCBvPRe6CVft/yHISE9UL7sflQnelBVdLO5Miy9MEZDRJUVCY
TwIDAQAB
-----END PUBLIC KEY-----"""

MONEYMOUR_PUBLIC_KEY_SANDBOX = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0A0WavOzsKJn0SHdQrF1
ThSdWly629clB6y4crZ0D778rQGmBFSkvdceIt3fERGYuCyWHFtiOS6pIlfIcJgR
hDoA0N6UKlT777KH8s/B3+cMnEHhPBiD0Lq8w8yjWdal1BvFkuUOionNm9q9OA2g
uD4BWv9WZBm1/mB7kNczvEGxvN1E601lJztU8WahWH1w0fEmRsW9BpcVrqlqfkuw
hPUnjeVXWDTX05gVyAr/Do6yNcJi6M5/4hU6EcQiQ+d1pHgd/mCLN/hoiPvGG5y9
UrR2av3bgfefF5QU7ZRzjMV3X7bGXPG2pH+L8kbHCPB78j5rzxHViSKIpPKkMg+P
FwIDAQAB
-----END PUBLIC KEY-----"""


class Signature:
    @staticmethod
    def build(private_key, expires_at, body):
        """
        Build a Moneymour APIs signature based on the given expires_at and body.

        :param private_key: Your personal private key
        :param expires_at: EPOCH timestamp
        :param body: The body to be sent in the POST request
        :return: A base64 encoded signature string
        """

        payload = Signature.build_payload(expires_at, body)

        rsa_key = RSA.importKey(private_key)
        signer = PKCS1_v1_5.new(rsa_key)

        signature = signer.sign(SHA256.new(payload.encode('utf-8')))

        return base64.b64encode(signature)

    @staticmethod
    def verify(signature, expires_at, body, public_key=None, environment=environments.ENVIRONMENT_SANDBOX):
        """
        Verify the given signature based on the given expires_at and body

        :param signature: The base64 encoded signature string
        :param expires_at: EPOCH timestamp
        :param body: The body to be sent in the POST request
        :param public_key: The RSA public key related to the RSA private key used for the signature
        :param environment: The API environment: production, sandbox, stage or development. Default: sandbox
        :return: True or False
        """

        if public_key is None:
            environments.validate_environment(environment)
            public_key = Signature.get_environment_public_key(environment)

        payload = Signature.build_payload(expires_at, body)

        rsa_key = RSA.importKey(public_key)
        signer = PKCS1_v1_5.new(rsa_key)
        digest = SHA256.new(payload.encode('utf-8'))

        return signer.verify(digest, base64.b64decode(signature))

    @staticmethod
    def get_environment_public_key(environment):
        """
        Get the public key related to the given environment name
        :param environment: The environment name in string format
        :return: The Moneymour RSA public ket for the given environment
        """

        environments.validate_environment(environment)

        return {
            'MONEYMOUR_PUBLIC_KEY_DEVELOPMENT': MONEYMOUR_PUBLIC_KEY_DEVELOPMENT,
            'MONEYMOUR_PUBLIC_KEY_STAGE': MONEYMOUR_PUBLIC_KEY_STAGE,
            'MONEYMOUR_PUBLIC_KEY_SANDBOX': MONEYMOUR_PUBLIC_KEY_SANDBOX
        }.get('MONEYMOUR_PUBLIC_KEY_' + environment.upper())

    @staticmethod
    def build_payload(expires_at, body):
        """
        Build the payload to be signed

        :param expires_at: EPOCH timestamp
        :param body: The body to be sent in the POST request
        :return: The payload to be signed in string format
        """

        return str(expires_at) + '|' + json.dumps(body, separators=(',', ':'), ensure_ascii=False)

    @staticmethod
    def generate_expires_at_header_value():
        """
        Generate a 60-second valid expires-at header value.

        :return: string EPOCH timestamp. Now UTC + 60 secondsw
        """
        return (datetime.now() + timedelta(seconds=60)).strftime('%s')
