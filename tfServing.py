import requests
import json

_server = "127.0.0.1:"

ports = {'pet': '8503',
         'can': '8501'}

url = 'http://'+_server

server_path = '/v1/models/recycle_'

headers = {"content-type": "application/json"}

# reqFunctions = {'pet': reqPET,
#                 'can': reqCan}


def reqToServer(recycleType,img):
    reqFunctions = {'pet': reqPET,'can': reqCan}
    reqTo = reqFunctions[recycleType] # 적절한 함수를 가져와서
    return reqTo(recycleType,img) # 실행결과를 return


def reqPET(recycleType,img) : #PET 모델에 request할 func
    specified_url = url+ports[recycleType]+server_path+recycleType+':predict'
    json_response = requests.post(specified_url, data=img, headers=headers)
    predictions = json_response.json()
    result = predictions['predictions']
    # 2차원 리스트로 차원 낮추기
    results = sum(result,[])

    # [0.0091186082, 0.00606526947, 0.0375309959, 0.0488448329, 1.39943268e-05, 0.679534197, 0.168709919]
    # detection box x 좌표, y, box의 width, height, confidence, 클래스 1(can)에 대한 확률, 클래스 2(distorted)에 대한 확률
    # 이 데이터 한 덩어리가 리스트로 여러 개 존재함
    correct = []
    # confidence에 대해 임의의 threshold를 넘으면 그 데이터를 이 리스트에 넣는다.
    for i in range(len(results)):
        if (results[i][4] > 0.4): # threshold for confidence = 0.4
            correct.append(results[i])
    # correct가 비어있으면 fail, 객체 감지부터가 안된거
    if (len(correct) == 0):
        # print('no object detected')
        return 'no object detected'
    for i in range(len(correct)):
        if (correct[i][6] > 0.8): # threshold for class probability (일단 can에 대한 확률로 해둠)
            return 'success'
    return 'fail'

def reqCan(recycleType,img) : #can model에 request할 func
    print('Request to can model detected')
    specified_url = url+ports[recycleType]+server_path+recycleType+':predict'
    json_response = requests.post(specified_url, data=img, headers=headers)
    predictions = json_response.json()
    result = predictions['predictions']
    # 2차원 리스트로 차원 낮추기
    results = sum(result,[])

    # [0.0091186082, 0.00606526947, 0.0375309959, 0.0488448329, 1.39943268e-05, 0.679534197, 0.168709919]
    # detection box x 좌표, y, box의 width, height, confidence, 클래스 1(can)에 대한 확률, 클래스 2(distorted)에 대한 확률
    # 이 데이터 한 덩어리가 리스트로 여러 개 존재함
    correct = []
    # confidence에 대해 임의의 threshold를 넘으면 그 데이터를 이 리스트에 넣는다.
    for i in range(len(results)):
        if (results[i][4] > 0.4): # threshold for confidence = 0.4
            correct.append(results[i])
    # correct가 비어있으면 fail, 객체 감지부터가 안된거
    if (len(correct) == 0):
        return 'no object detected'
    for i in range(len(correct)):
        if (correct[i][6] > 0.8): # threshold for class probability (일단 can에 대한 확률로 해둠)
            return 'success'
    return 'fail'