# Comment added
import requests
import json
import time
import uuid

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
uniqueid = str(uuid.uuid4())
timestamp_for_file_name = uniqueid +'.txt'
logfile = 'log_' + uniqueid+'.csv'
f = open(logfile, "a")
f.write("timestamp,riskdatacatagory,url,httpstatuscode,recordcount,details\n")
f.close()


def logevents(riskdatacatagory, url, httpstatuscode, recordcount, details):
	f = open(logfile, "a")
	content = time.strftime("%Y%m%d-%H%M%S")+","+riskdatacatagory+','+url+","+httpstatuscode+","+recordcount+","+details + "\n"
	f.write(content)
	f.close()
	print(content)


def getRiskData(riskdatacatagory, url, json_data, filename):
	print(url)
	nextpageurl = ''
	alldata = []
	filename_counter = 1
	if not json_data['access_token'] is None:
		while True:
			responseheaders = ''
			riskEventData = ''
			headerparams = {'Authorization':json_data['token_type']+" "+json_data['access_token']}
			tries = 10
			retryafter = 10
			for i in range(tries):
				riskEventData = requests.get(url, headers=headerparams,verify=False)
				if riskEventData.status_code == 429:
					retryafter = int(riskEventData.headers.get("Retry-After"))
					logevents(riskdatacatagory, url, str(riskEventData.status_code), "0", "Too many requests error.")
					if i < tries - 1:
						logevents(riskdatacatagory, url, "", "", 'Sleeping for ' + str(retryafter)+' second(s).')
						time.sleep(retryafter)
						logevents(riskdatacatagory, url, "", "", 'Well slept!! Retry again...')
						continue
					else:
						raise
				break
			try:
				rawjson = riskEventData.json()
				if 'value' in rawjson and len(rawjson['value'])>0:
					m = json.dumps(rawjson['value'])
					alertsjson = json.loads(m)
					print(str(alertsjson))
					logevents(riskdatacatagory, url, str(riskEventData.status_code), str(len(alertsjson)), "Request successful")
					alldata = alldata + alertsjson
					if '@odata.nextLink' not in rawjson:
						break;
					
					nextpageurl = json.dumps(rawjson['@odata.nextLink'])
					nextpageurl =  nextpageurl.replace("\"","")
					url = nextpageurl
			except:
				a = 0
	with open(filename, 'w') as outfile:
		json.dump(alldata, outfile)

	logevents(riskdatacatagory, url, str(riskEventData.status_code), str(len(alldata)), "Total record(s) : " + str(len(alldata)))


clientid = "YOUR CLIENT ID"
clientsecret = "YOUR CLIENT SECRET"
tenantdomain = "YOUR DOMAIN NAME"
loginurl = "https://login.microsoft.com"
resource = "https://graph.microsoft.com"

identityRiskEventsURL = "https://graph.microsoft.com/beta/identityRiskEvents"
signInEventsURL = "https://graph.microsoft.com/beta/auditLogs/signIns?$filter=createdDateTime ge 2018-12-25"
identityRiskyUsersURL = "https://graph.microsoft.com/beta/riskyUsers"
riskDetectionsURL = "https://graph.microsoft.com/beta/riskDetections"

body = {'grant_type':'client_credentials','resource':resource,'client_id':clientid,'client_secret':clientsecret}
posturl = loginurl+"/"+tenantdomain+"/oauth2/token?api-version=1.0"
print("Posting data to get OAuth token")
oauth = requests.post(posturl, data=body, verify=False)
json_data = oauth.json()
print("Got OAuth token")


#getRiskData('IdentityRiskEvent',identityRiskEventsURL,json_data,'identityrisk_'+timestamp_for_file_name)

getRiskData('RiskyUserEvent', identityRiskyUsersURL, json_data,'riskyuser_'+timestamp_for_file_name)
getRiskData('RiskDetection', riskDetectionsURL, json_data, 'riskdetections_'+timestamp_for_file_name)

# Need to put filter in the signIn event to a avoid huge number of records
#getRiskData('SignInEvent', signInEventsURL, json_data, 'signIn_'+timestamp_for_file_name)
