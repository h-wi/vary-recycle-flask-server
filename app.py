from flask import Flask,request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from werkzeug.utils import secure_filename
import preprocess as prepro
import tfServing as tf
import firebaseReq as fireReq
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
import time

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록
scheduler = BackgroundScheduler()
scheduler.add_job(func=fireReq.resetCount, trigger='cron', hour=23, minute=59, second=58)
scheduler.start()         

@app.route('/test', methods=['POST','GET'])
def test():
    try :
        uid = request.json[0]['uid']
        base64Image = request.json[0]['image']
        recycleType = request.json[0]['type']

        willPass=fireReq.willAccept(uid)
        if willPass !='True':
            return willPass

        input_img=prepro.preprocessImage(base64Image)
        result=tf.reqToServer(recycleType,input_img)

        if result == 'success':
            if fireReq.success(uid) != True:
                return 'Failed to update credit'
        return result

    except :
        return 'Failed to execute server'


@api.route('/hello')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
            