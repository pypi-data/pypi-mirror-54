import json
import time
from typing import List, Dict

import jwt

from ..aws_secret import AwsSecret


class DCPServiceAccountManager:
    """
    Manage the minting of JWT for making authenticated request from DCP service account.

    A DCPServiceAccountManager can be created from a service credentials stored in AWS or from a in a file stored
    locally. The prefered method is to store in a secret in AWS.

    Authorization headers are generated by calling DCPServiceAccountManager.get_authorization_header. This header
    should be added to the request header of an https request to authenticate the requester.
    """
    _default_renew_buffer = 30
    _default_lifetime = 3600
    _options = {
        'verify_signature': False,
        'verify_aud': False,
        'verify_iss': False
    }

    # options used to check expiration of token.

    @classmethod
    def from_secrets_manager(cls, secret_id, audience, **kwargs):
        """
        Retrieve the secretId stored in AWS secrets manager and create a DCPServiceAccountManager.

        :param secret_id: The secretId store in AWS secrets manager
        :param audience: The audience to use in the JWT
        :param kwargs: arguments passed to the DCPServiceAccountManager.__init__ method
        :return:
        """
        credentials = json.loads(AwsSecret(secret_id).value)
        return cls(credentials, audience, **kwargs)

    @staticmethod
    def format_secret_id(secret_name: str, deployment: str = '', service: str = '') -> str:
        """

        :param secret_name: the name of the secret.
        :param deployment: the deployment the secret is stored in.
        :param service: the service the secret is for.
        :return: A secretId formatted using the dcp format for secrets.
        """
        return '/'.join([i for i in ['dcp', service, deployment, secret_name] if i])

    def __init__(self,
                 google_service_account_credentials: dict,
                 audience: List[str],
                 additional_claims: Dict = None,
                 renew_buffer: int = None,
                 lifetime: int = None):
        """

        :param google_service_account_credentials: a json dict containing google service account credentials.
        :param audience: the audience used for the managed JWT.
        :param additional_claims: additional claims added to the managed JWT.
        :param renew_buffer: (seconds) If the JWT will expire in less than this amount of time, generate a new JWT.
        :param lifetime: (seconds) how long the token should live.
        """

        self.credentials = google_service_account_credentials
        self.audience = audience
        self.additional_claims = additional_claims
        self.renew_buffer = renew_buffer or self._default_renew_buffer
        self.lifetime = lifetime or self._default_lifetime
        self.token = None

    def get_authorization_header(self):
        """
        Generate an authorization header using the audience and additional claims specified during the objects
        initialization.

        :return: an authorization header for making authenticated requests to DCP components.
        """
        return {"Authorization": "Bearer {}".format(self.get_jwt())}

    def create_authorization_header(self, **kwargs):
        """
        Generates a new JWT with the kwargs provided and returns it in an authorization header. Use this function
        when you need to generate a head that does not use the audience or additional_claims specified when the
        object was initialized.
        :param kwargs: arguments passed through to create_jwt
        :return: an authorization header for making authenticated requests to DCP components.
        """
        return {"Authorization": "Bearer {}".format(self.create_jwt(**kwargs))}

    def get_jwt(self):
        """
        Generate and manages JWT token. A new JWT is minted when the current JWT expires.
        """
        if self.token is None or self.is_expired(self.token):
            self.token = self.create_jwt(self.audience, self.additional_claims)
        return self.token

    def create_jwt(self, audience: List[str], additional_claims=None) -> str:
        """
        Creates a JWT using the supplied audience and additional_claims parameters

        :param audience:
        :param additional_claims:
        :return:
        """
        iat = time.time()
        exp = iat + self.lifetime
        payload = additional_claims or {}
        payload.update({'iss': self.credentials["client_email"],
                        'sub': self.credentials["client_email"],
                        'aud': audience,
                        'iat': iat,
                        'exp': exp,
                        'scope': ['email', 'openid', 'offline_access'],
                        'email': self.credentials["client_email"]
                        })
        additional_headers = {'kid': self.credentials["private_key_id"]}
        token = jwt.encode(
            payload,
            self.credentials["private_key"],
            headers=additional_headers,
            algorithm='RS256').decode()
        return token

    def is_expired(self, token: str) -> bool:
        """
        Check if the provided token has expired.

        :param token: a JWT
        :return:
        """
        try:
            decoded_token = jwt.decode(token, options=self._options)
        except jwt.ExpiredSignatureError:  # type: ignore
            return True
        else:
            if decoded_token['exp'] - time.time() >= self.renew_buffer:
                # If the token will expire in less than cls._renew_buffer amount of time in seconds, the token is
                # considered expired.
                return True
            else:
                return False
