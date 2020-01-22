# Azure AD Identity Protection
This python script uses the ClientId, Client Secret (configured in Azure portal) and the tenant domain to
get the OAuth token and then uses the OAuth token to query the Microsoft Graph API 
to get the identity protection data in the JSON format for both risky users and risky detection.

The code also retries in case of the number of requests crosses the threshold ( i.e when the request fails with HTTP status code 429- "Too many requests").

Creates two types of output files :
1) CSV log files for the request status to the Microsoft Graph API
2) JSON output files for indivisual requests with prefix - "riskyuser_", "riskdetections_", "identityrisk_"

**Example for riskDetectin JSON**

```
[
{
		"id": "10c2017481bfae5f519a0ac52253b84dc4647bafaf19951a",
		"requestId": "0bf9f8-0363-411b-9a85-42b34f8b6e00",
		"correlationId": "6d2c4537-6658-4f6b-bd83-608873a623e7",
		"riskType": "anonymizedIPAddress",
		"riskState": "atRisk",
		"riskLevel": "medium",
		"riskDetail": "none",
		"source": "IdentityProtection",
		"detectionTimingType": "realtime",
		"activity": "signin",
		"tokenIssuerType": "AzureAD",
		"ipAddress": "107.181.166.170",
		"activityDateTime": "2019-10-24T15:52:59.2544431Z",
		"detectedDateTime": "2019-10-24T15:52:59.2544431Z",
		"lastUpdatedDateTime": "2019-10-24T15:54:01.1560141Z",
		"userId": "3461fa0b-612e-4805-942d-0d5b9f3647f7",
		"userDisplayName": "John Doe",
		"userPrincipalName": "john.doe@example.com",
		"additionalInfo": "[{\"Key\":\"userAgent\",\"Value\":\"accountsd/113 CFNetwork/978.0.7 Darwin/18.7.0 (x86_64)\"}]",
		"location": {
			"city": "San Jose",
			"state": "California",
			"countryOrRegion": "US",
			"geoCoordinates": {
				"latitude": 31.38745,
				"longitude": -123.9023
			}
		}
	},
	{
		"id": "9b8d3a520856b1b9f9f31c651c47a86c65a04cc35d593824c6af1de42f50832e",
	  ....
  }
]
```

**Example for Risky User JSON response **
```
[
	{
		"id": "ddebe803-8acf-4ff5-8d6f-f51dd844ca88",
		"isDeleted": false,
		"isGuest": false,
		"isProcessing": false,
		"riskLevel": "high",
		"riskState": "atRisk",
		"riskDetail": "none",
		"riskLastUpdatedDateTime": "2020-01-08T07:13:46.0524129Z",
		"userDisplayName": "Doe, John",
		"userPrincipalName": "john.doe@example.com"
	},
	{
		"id": "ddebe803-8acf-4ff5-8d6f-f51dd844caa8",
	  ....
  }
]
