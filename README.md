# AzureADIdentityProtection
This python script uses the ClientId, Client Secret (configured in Azure portal) and the tenant domain to
get the OAuth token and then uses the OAuth token to query the Microsoft Graph API 
to get the identity protection data in the JSON format for both risky users and risky detection.

The code also retries in case of the number of requests crosses the threshold (HTTP 429 Too many requests).
