import requests
import json

from moneymour import environments
from moneymour.crypto_utils import Signature

API_BASE_URL = 'https://api.moneymour.com'
API_SANDBOX_BASE_URL = 'https://api.sandbox.moneymour.com'
API_STAGE_BASE_URL = 'https://api.stage.moneymour.com'
API_DEVELOPMENT_BASE_URL = 'http://localhost:3000'

ENDPOINT_MERCHANT_REQUEST = '/merchant-request'


class ApiClient:
    def __init__(self, merchant_id, merchant_secret, environment=environments.ENVIRONMENT_SANDBOX):
        environments.validate_environment(environment)

        self.merchant_id = merchant_id
        self.merchant_secret = merchant_secret
        self.environment = environment

    def request(self, private_key, body):
        """
        Request a loan.

        :param private_key: Your personal private key
        :param body: The body to be sent in the POST request
        :return: JSON decoded object
        """
        
        # Add identification fields to the request
        body['merchantId'] = self.merchant_id
        body['secret'] = self.merchant_secret

        expires_at = Signature.generate_expires_at_header_value()
        signature = Signature.build(private_key, expires_at, body)

        headers = {
            'Content-Type': 'application/json',
            'Expires-at': expires_at,
            'Signature': signature.decode("utf-8")
        }

        body = json.dumps(body, separators=(',', ':'))

        # Perform the request
        r = requests.post(ApiClient.get_api_base_url(self.environment) + ENDPOINT_MERCHANT_REQUEST, headers=headers,
                          data=body)

        return json.loads(r.text)

    @staticmethod
    def get_api_base_url(environment):
        environments.validate_environment(environment)

        if environment == environments.ENVIRONMENT_PRODUCTION:
            return API_BASE_URL
        elif environment == environments.ENVIRONMENT_SANDBOX:
            return API_SANDBOX_BASE_URL
        elif environment == environments.ENVIRONMENT_STAGE:
            return API_STAGE_BASE_URL
        else:
            return API_DEVELOPMENT_BASE_URL
