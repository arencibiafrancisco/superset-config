import logging
from superset.security import SupersetSecurityManager

class CustomSsoSecurityManager(SupersetSecurityManager):
    """
    Custom Security Manager for handling Azure OAuth2 authentication.
    """

    def oauth_user_info(self, provider, response=any):
        """
        Extracts user information from the OAuth2 response provided by Azure.

        Args:
            provider (str): The name of the OAuth2 provider (e.g., 'azure').
            response (dict): The response object from the OAuth2 provider.

        Returns:
            dict: A dictionary containing user information like name, email,
                  username, and roles.
        """
        logging.debug("Oauth2 provider: {0}.".format(provider))

        if provider == 'azure':
            # Decode and validate the JWT token from Azure
            me = self._decode_and_validate_azure_jwt(response["id_token"])
            logging.debug("user_data: {0}".format(me))

            # Map the user data fields to a standardized format
            return {
                'name': me['upn'],
                'email': me['upn'] if "upn" in me else me['email'],
                'id': me['upn'],
                'username': me['upn'] if "upn" in me else me['email'],
                'first_name': me['given_name'],
                'last_name': me['family_name'],
                'role_keys': me.get('roles', []),  # Optional roles, default to an empty list
            }
