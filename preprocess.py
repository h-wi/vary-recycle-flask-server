from tensorflow import keras
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import requests
import json
# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1

def preprocessImage(inputImg) :
    # float타입 값을 가질 수 있는 640x640의 3차원 빈 Tensor 1개 생성 
    reqData = np.ndarray(shape=(1, 640, 640, 3), dtype=np.float32)
    
    # 받아온 이미지를 640x640으로 맞추기(YOLOv5)
    size = (640, 640)
    image = ImageOps.fit(inputImg, size, Image.Resampling.LANCZOS)
    
     # turn the image into a numpy array (640x640x3)
    image_array = np.asarray(image)
    
    # Normalize the image (RGB니까 255로 nomalized)
    normalized_image_array = (image_array.astype(np.float32) / 225.0)     
    
    # Load the image into the array (그대로 복붙)
    reqData = normalized_image_array
    
    reqData = np.expand_dims(reqData,axis=0)

    #########################################################
    # YOLO모델은 텐서에 batch dimension이 필요해서 아마 안될 것 같긴한데..
    # 이 코드는 (640,640,3)을 보내는 코드인데 안되면 맨 앞에 batch dimension 추가해야 
    data = json.dumps({"instances": reqData[0:4].tolist()}) 
    
    #######################################################
    return data