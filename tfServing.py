import requests
import json

def reqToServer(recycleType,img):
    _server = "127.0.0.1:8501"
    url = 'http://'+_server+'/v1/models/recycle:predict'
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=img, headers=headers)
    predictions = json_response.json()
    result = predictions['predictions']
    print(result)
    if float(result[0][0])>float(result[0][1]) :
        return 'success'
    else :
        return 'fail'