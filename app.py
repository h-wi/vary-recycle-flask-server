from flask import Flask,request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from werkzeug.utils import secure_filename
import base64
import preprocess as prepro
import tfServing as tf
from PIL import Image
import numpy as np
import cv2

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록


@api.route('/hello')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

@app.route('/test', methods=['POST','GET'])
def test():
    base64Image = request.json[0]['image']
    recycleType = request.json[0]['type']
    imageStr = base64.b64decode(base64Image)
    # base64 형식의 이미지
    nparr = np.fromstring(imageStr, np.uint8)
    # String 형태의 imageStr을 NumPy Tensor Array로 변환
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1
    # nuarr의 color 데이터를 img_np에 새롭게 load
    img_cvt = cv2.cvtColor(img_np , cv2.COLOR_BGR2RGB)
    # BGR형식의 color를 RGB 형식으로 Convert
    img = Image.fromarray(img_cvt)
    # 이미지의 각 픽셀에 대응하는 값을 가진 Array(img_cvt)를 통해 이미지 생성
    img = img.convert("RGB")
    # RGB 변환? 이미 하지 않았나

    input_img=prepro.preprocessImage(img) #image 형태로 넘긴다?
    result=tf.reqToServer(recycleType,input_img)
    return result

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
