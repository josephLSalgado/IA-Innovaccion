import urllib
import urllib.request
import json 

data =  {

        "Inputs": {

                "input1":
                {
                    "ColumnNames": ["WallArea", "RoofArea", "OverallHeight", "GlazingArea", "HeatingLoad"],
                    "Values": [ [ "296", "110.25", "7", "0", "15.55" ], [ "400", "93.25", "1", "0", "23.55" ], ]
                },        },
            "GlobalParameters": {
}
    }

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/b1675693baaa45b3b159b2836951deca/services/fed9c92a51b5450fbc6f9f74518c0991/execute?api-version=2.0&details=true'
api_key = 'API_KEY'
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers) 

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result) 
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())

    print(json.loads(error.read()))                 