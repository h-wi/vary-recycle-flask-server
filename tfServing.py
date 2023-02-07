import requests
import json

_server = "127.0.0.1:"

ports = {'pet': '8503',
         'can': '8501'} # Add GLA and PAP

url = 'http://'+_server

server_path = '/v1/models/recycle_'

headers = {"content-type": "application/json"}

######################## tuning thresholds #############################
CONFIDENCE = 0.4 # threshold for confidence 

PET_LABEL_PROBABILITY = 0.5 #페트병 라벨으로 예상할 확률
PET_LID_PROBABILITY = 0.5 #페트병 뚜껑

CAN_PROBABILITY = 0.6 #찌그러진 캔으로 예상할 확률

GLA_CONTENT_PROBABILITY = 0.3 #유리병의 내용물로 예상할 확률
GLA_PROBABILITY = 0.6 # 유리병으로 예상할 확률

PAP_PROBABILITY = 0.6
##################################################################


def reqToServer(recycleType,img):
    specified_url = url+ports[recycleType]+server_path+recycleType+':predict'
    json_response = requests.post(specified_url, data=img, headers=headers)
    predictions = json_response.json()
    result = predictions['predictions']
         
    # 2차원 리스트로 차원 낮추기
    results = sum(result,[])

    # Example. [0.0091186082, 0.00606526947, 0.0375309959, 0.0488448329, 1.39943268e-05, 0.679534197, 0.168709919]
    # detection한 box x 좌표, y, box의 width, height, confidence, 클래스 1(can)에 대한 확률, 클래스 2(distorted)에 대한 확률
    # 이 데이터 한 덩어리가 리스트로 여러 개 존재함, 클래스 개수에 따라 이 덩어리가 늘어난다.

    # confidence에 대해 임의의 threshold를 넘으면 그 데이터를 이 리스트에 넣는다.
    correct = []
    
         
    for i in range(len(results)):
        if (results[i][4] > 0.4): # threshold for confidence 
            correct.append(results[i])
    if (len(correct) == 0):
        return 'no object detected'
    # correct가 비어있으면 fail, 객체 감지부터가 안된거 ; 여기까진 모든 모델이 똑같음
    
    for i in range(len(correct)):
        if (recycleType == 'pet'): # 5: distorted, 6: label, 7 : lid
         if (correct[i][6] < PET_LABEL_PROBABILITY && correct[i][7] > PET_LID_PROBABILITY):
                  return 'success'
        elif (recycleType == 'can'):
         if (correct[i][6] > CAN_PROBABILITY):
                  return 'success'
        elif (recycleType == 'gla'):
         if (correct[i][5] < GLA_CONTENT_PROBABILITY && GLA_PROBABILITY):
                  return 'success'
        elif (recycleType == 'pap'):
         if (correct[i][5] > PAP_PROBABILITY || correct[i][6] > PAP_PROBABILITY):
                  return 'success'
         
    return 'fail' # 아무것도 안되면 fail
