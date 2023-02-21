import requests
import json

url = 'http://127.0.0.1:8501/v1/models/'

headers = {"content-type": "application/json"}

######################## tuning thresholds #############################
CONFIDENCE = 0.8 # threshold for confidence 

PET_LABEL_PROBABILITY = 0.5 #페트병에 라벨이 붙어있다고 예상할 확률
PET_DISTORT_PROBABILITY = 0.5 #페트병이 찌그러졌는지 예상할 확률

#######################################################################

# temporal 
CAN_PROBABILITY = 0.6 #찌그러진 캔으로 예상할 확률

GLA_CONTENT_PROBABILITY = 0.3 #유리병의 내용물로 예상할 확률
GLA_PROBABILITY = 0.6 # 유리병으로 예상할 확률

PAP_PROBABILITY = 0.6
# until here



def reqToServer(recycleType,img):
    try :
        specified_url = url+recycleType+':predict'
        json_response = requests.post(specified_url, data=img, headers=headers)
        predictions = json_response.json()
        result = predictions['predictions']
    except :
        print('[Error] : Failed to get response from server')
        return 'fail'

    try :
        # 2차원 리스트로 차원 낮추기
        results = sum(result,[])

        # Example about 'results' : [0.0091186082, 0.00606526947, 0.0375309959, 0.0488448329, 1.39943268e-05, 0.679534197, 0.168709919]
        # detection한 box x 좌표, y, box의 width, height, confidence, 클래스 1(can)에 대한 확률, 클래스 2(distorted)에 대한 확률
        # 이 데이터 한 덩어리가 리스트로 여러 개 존재함, 클래스 개수에 따라 이 덩어리가 늘어난다.
        
        correct = []
        
        # confidence에 대해 임의의 threshold를 넘으면 그 데이터를 이 리스트(correct)에 넣는다.
        # correct가 비어있으면 fail, 객체 감지부터가 안된거 ; 여기까진 모든 모델이 똑같음
        for i in range(len(results)):
            if (results[i][4] > 0.4): # threshold for confidence 
                correct.append(results[i])
        if (len(correct) == 0):
            return 'no object detected'
        
        model_results = {} # 더 많은 정보를 보내기 위해 Dictionary로 반환하기
        
        model_results['result'] = ''
        model_results['success'] = 0
        model_results['fail'] = 0
        model_results['detected_object'] = len(correct) # len(correct) : 감지된 물체의 개수
        model_results['fail_coordinates'] = []
        
        for i in range(len(correct)):
            if (recycleType == 'pet'): # 5: distorted, 6: label, 7 : lid
                
                if (correct[i][5] > PET_DISTORT_PROBABILITY and correct[i][6] < PET_LABEL_PROBABILITY):
                    model_results['success'] += 1
                else:
                    model_results['fail'] += 1
                    correct[i].append('recycleType')
                    model_results['fail_coordinates'].append(correct[i])
                    
            elif (recycleType == 'can'): # 5: can 6: distorted
                
                if (correct[i][6] > CAN_PROBABILITY):
                    model_results['success'] += 1
                else:
                    model_results['fail'] += 1
                    correct[i].append('recycleType')
                    model_results['fail_coordinates'].append(correct[i])
                    
            elif (recycleType == 'glass'): #5 : content
                
                if (correct[i][5] < GLA_CONTENT_PROBABILITY and GLA_PROBABILITY):
                    model_results['success'] += 1
                else:
                    model_results['fail'] += 1
                    correct[i].append('recycleType')
                    model_results['fail_coordinates'].append(correct[i])
                    
            elif (recycleType == 'paper'): # 5 : paper # 6 : cardbox
                
                if (correct[i][5] > PAP_PROBABILITY or correct[i][6] > PAP_PROBABILITY):
                    model_results['success'] += 1
                else:
                    model_results['fail'] += 1
                    correct[i].append('recycleType')
                    model_results['fail_coordinates'].append(correct[i])
        
        if (model_results['success'] > 0): # 1개라도 성공하면 success로 보냄
            model_results['result'] = 'success'
        else:
            model_results['result'] = 'fail'
            
        return model_results['result']
    except :
        print("[Error] : Wrong response from ML model server")
        return 'fail'    
