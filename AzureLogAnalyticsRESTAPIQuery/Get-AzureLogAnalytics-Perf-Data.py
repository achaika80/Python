#import modules region

import requests, urllib3, json
import pandas as pd
from pandas.io.json import json_normalize
from datetime import datetime
from datetime import timedelta
import plotly.express as px
import re

#variables region

workspaceid = '<>'
# Tenant ID for your Azure subscription
TENANT_ID = '<>'
# Your service principal App ID
CLIENT = '<>'
# Your service principal password
KEY = '<>'

loginURL = "https://login.microsoftonline.com/" + TENANT_ID + "/oauth2/token"
resource = "https://api.loganalytics.io"
url = "https://api.loganalytics.io/v1/workspaces/" + workspaceid + "/query"

StartDateTime = datetime.strptime('2020-10-22 00:00:00', '%Y-%m-%d %H:%M:%S')
StartDateTime = StartDateTime + timedelta(hours=4)
EndDateTime = datetime.strptime('2020-10-30 00:00:00', '%Y-%m-%d %H:%M:%S')
EndDateTime = EndDateTime + timedelta(hours=4)
servername = '<>'

#saving query parameters to the array of query dicts
queryParam = [
    {
        'Computer':servername,
        'CounterName':'% Privileged Time',
        'ObjectName':'Processor',
        'InstanceName':''
    },
    {
        'Computer':servername,
        'CounterName':'% User Time',
        'ObjectName':'Processor',
        'InstanceName':''
    },
    {
        'Computer':servername,
        'CounterName':'Processor Queue Length',
        'ObjectName':'System',
        'InstanceName':''
    },
    {
        'Computer':servername,
        'CounterName':'Available Bytes',
        'ObjectName':'Memory',
        'InstanceName':''
    },
    {
        'Computer':servername,
        'CounterName':'Pages/sec',
        'ObjectName':'Memory',
        'InstanceName':''
    }
]

#get authorizartion token function

def get_token(url, resource, Username, Password):
    payload = {
        'grant_type': 'client_credentials',
        'client_id': Username,
        'client_secret': Password,
        'Content_Type': 'x-www-form-urlencoded',
        'resource': resource,
    }
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    ApiReturn = requests.post(url, data=payload, verify=False)
    ApiToken = json.loads(ApiReturn.content)["access_token"]
    return { "Authorization": str("Bearer "+ ApiToken), 'Content-Type': 'application/json'}


def createQueries(queryParam):
    #creating array for queries
    queries = []
    #iterating through list of query parameters dicts 
    for query in queryParam:
        if query['InstanceName']:
            queries.append((f"Perf | where TimeGenerated between(datetime({StartDateTime}) .. datetime({EndDateTime})) "
                f"and Computer == '{query['Computer']}' and CounterName == '{query['CounterName']}' "
                f"and ObjectName == '{query['ObjectName']}' and InstanceName == '{query['InstanceName']}' "
                "| extend ET_TimeGenerated = TimeGenerated - 4h "
                "| project Computer, ObjectName, CounterName, InstanceName, CounterValue, TimeGenerated, ET_TimeGenerated"))
        else:
            queries.append((f"Perf | where TimeGenerated between(datetime({StartDateTime}) .. datetime({EndDateTime})) "
                f"and Computer == '{query['Computer']}' and CounterName == '{query['CounterName']}' "
                f"and ObjectName == '{query['ObjectName']}' "
                "| extend ET_TimeGenerated = TimeGenerated - 4h "
                "| project Computer, ObjectName, CounterName, InstanceName, CounterValue, TimeGenerated, ET_TimeGenerated"))
    return queries

def getlogdata(query):
    
    #getting auth token to use with request
    Headers = get_token(loginURL, resource, CLIENT, KEY)
    
    params = {
       "query": query
    }

    result = requests.get(url, params=params, headers=Headers, verify=False)
    print(f"REST API request: {result}")
    JSONContent = result.json()
    columns = len(result.json()['tables'][0]['columns'])
    dtcolumns =[]
    for column in range(0,columns):
        dtcolumns.append(result.json()['tables'][0]['columns'][column]['name'])
    dtrows =[]
    dtrows = (result.json()['tables'][0]['rows'])
    df=pd.DataFrame(dtrows)
    df= pd.DataFrame(dtrows, columns=dtcolumns)
    df.sort_values(by=['ET_TimeGenerated'],inplace=True)
    if {'CounterValueMB'}.issubset(df.columns):
        df.drop(columns=['CounterValue'],inplace=True)
        df.rename(columns={"CounterValueMB":"CounterValue"},inplace=True)
    return df

def drawgraph(df):
    figtitle = servername + " - " + df['ObjectName'][0] + " - " + df['CounterName'][0]
    print(f"Now working on: {figtitle}")
    now = datetime.now()
    now = now.strftime("%d-%m-%Y-%H-%M-%S")
    if(df['InstanceName'][0]):
        lineColor = 'InstanceName'
    else:
        lineColor = 'CounterName'
    fileName = re.sub('[^a-zA-Z0-9\n\.]','',df['CounterName'][0])
    filepath = "/Users/Temp/PY/" + fileName + "-" + now +".html"
    fig = px.line(df, x = 'ET_TimeGenerated', y = 'CounterValue', title=figtitle, color=lineColor)
    fig.write_html(filepath)

queries = createQueries(queryParam)

for qstr in queries:
     df = getlogdata(qstr)
     df.reset_index(drop = True, inplace = True)
     drawgraph(df)
     now = datetime.now()
     now = now.strftime("%d-%m-%Y-%H-%M-%S")
     fileName = re.sub('[^a-zA-Z0-9\n\.]','',df['CounterName'][0])
     filepath = "/Users/Temp/PY/" + fileName + "-" + now +".csv"
     df.to_csv(filepath)


