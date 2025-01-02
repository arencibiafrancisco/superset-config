import logging
from superset.security import SupersetSecurityManager

class CustomSsoSecurityManager(SupersetSecurityManager):
    """
    Custom Security Manager for handling Azure OAuth2 authentication.
    """

    def oauth_user_info(self, provider, response):
        """
        Extracts user information from the OAuth2 response provided by Azure.

        Args:
            provider (str): The name of the OAuth2 provider (e.g., 'azure').
            response (dict): The response object from the OAuth2 provider.

        Returns:
            dict: A dictionary containing user information like name, email,
                  username, and mapped roles.
        """
        logging.debug(f"Oauth2 provider: {provider}")

        if provider == 'azure':
            # Decode and validate the JWT token from Azure
            me = self._decode_and_validate_azure_jwt(response["id_token"])
            logging.debug(f"User data from Azure: {me}")

            # Extract roles from Azure's JWT token
            azure_roles = me.get('roles', [])
            logging.debug(f"Roles from Azure: {azure_roles}")

            # Map Azure roles to Superset roles
            mapped_roles = []
            roles_mapping = {
                "superset_users": ["Gamma"],
                "superset_admins": ["Admin"],
            }
            for azure_role in azure_roles:
                for superset_role, azure_mapped_roles in roles_mapping.items():
                    if azure_role in azure_mapped_roles:
                        mapped_roles.append(superset_role)

            # Ensure roles are unique
            mapped_roles = list(set(mapped_roles))
            logging.debug(f"Mapped Superset roles: {mapped_roles}")

            # Map the user data fields to a standardized format
            return {
                'name': me['upn'],
                'email': me['upn'] if "upn" in me else me['email'],
                'id': me['upn'],
                'username': me['upn'] if "upn" in me else me['email'],
                'first_name': me['given_name'],
                'last_name': me['family_name'],
                'role_keys': mapped_roles,  # Mapped roles for Superset
            }
