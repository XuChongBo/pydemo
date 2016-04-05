import requests
import json

url = 'http://localhost:7001/api/v1.0/text/doRecognition.json'

appkey = "ae46e6ad-fe81-465d-bc38-6cae1d3fd0b2"

text_input = {
    "textParameter": {"language":"en_US", "textInputMode":"CURSIVE"},
        "inputUnits": [
            {
                "textInputType":"MULTI_LINE_TEXT",
                "components": [{
                    "type":"stroke", 
                    "x": [
                      438,
                      439,
                      439
                    ],
                   "y": [
                      319.5,
                      313.5,
                      312.5
                   ]
                }
             ]
          }
       ]
    }
data = {'applicationKey':appkey, 'textInput': json.dumps(text_input)}
response = requests.post(url=url, data=data)
print response.content
