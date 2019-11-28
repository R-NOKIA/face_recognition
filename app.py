from flask import Flask, request,Response
import face_recognition
from face_deal import FaceRecognition
from PIL import Image
import numpy as np
import json
import os
import time
app = Flask(__name__)
faceDeal = FaceRecognition()
#测试
@app.route('/')
def hello_world():
    return 'Hello World!'
#获取人脸信息，并存入个人本地时间文件
@app.route("/get_face_locations", methods=['POST'])
def get_face_locations():
    try:
        file = request.files['file']
    except:
        return json.dumps({"err_message": "file null"})
    try:
        name=request.values.get(u'name')
    except:
        return json.dumps({"err_message": "name null"})
    f = open('./face_location.jpg', 'wb')
    data = file.read()
    f.write(data)
    f.close()
    message=add_imagelist(file,data,name)
    if(message=='fail to add'):
        return json.dumps({"err_message": message})
    image_array = np.array(Image.open("./face_location.jpg").convert("RGB"))
    result = faceDeal.compare_face_token(image_array)
    os.remove("./face_location.jpg")
    print(result)
    if len(result.get('faces'))==0:
        return json.dumps({"err_message":"There is no face"})
    elif result.get('faces')[0].get("face_name")=='unknown':
        return json.dumps({"err_message":"The face is not exit"})
    else:
        return json.dumps(result)
# 接受图片返回人名
@app.route("/get_know_tokens", methods=['POST'])
def get_know_tokens():
    try:
        file = request.files['file']
    except:
        return json.dumps({"err_message": "file null"})
    f = open('./face_location.jpg', 'wb')
    data = file.read()
    f.write(data)
    f.close()
    image_array = np.array(Image.open("./face_location.jpg").convert("RGB"))
    result = faceDeal.compare_face_token(image_array)
    os.remove("./face_location.jpg")
    if len(result.get('faces')) == 0:
        return json.dumps({"err_message": "There is no face"})
    elif result.get('faces')[0].get("face_name") == 'unknown':
        return json.dumps({"err_message": "The face is not exit"})
    else:
        face_name=result.get('faces')[0].get("face_name")
        print(face_name)
        return json.dumps({"face_name":face_name})
# 注册时初始化
@app.route("/add_tokens", methods=['POST'])
def add_tokens():
    try:
        file = request.files['file']
    except:
        return json.dumps({"err_message": "wrong image file"})
    try:
        name=request.values.get(u'name')
    except:
        return json.dumps({"err_message": "name null"})
    f = open('./add_token.jpg', 'wb')
    data = file.read()
    f.write(data)
    f.close()
    image_array = np.array(Image.open("./add_token.jpg").convert("RGB"))
    os.remove("./add_token.jpg")
    try:
        faceDeal.add_face_token(image_array,name)
        return json.dumps({"suc_message": "success"})
    except:
        return json.dumps({"err_message": "fail to load file,may change"})
# 添加一张注册用图片
@app.route('/add_images',methods=['POST'])
def up_load_img():
    try:
        file = request.files['file']
    except:
        return json.dumps({"err_message": "wrong image file"})
    try:
        name = request.values.get(u'name')
    except:
        return json.dumps({"err_message": "name null"})
    imagetype=str(file.filename).split('.')[1]
    try:
        f = open('./static/image/'+name+'.'+imagetype, "wb")
        f.write(file.read())
        f.close()
        if len(face_recognition.face_encodings(face_recognition.load_image_file('./static/image/'+name+'.'+imagetype)))<1:
             return json.dumps({"err_message": "fail to add"})
        return json.dumps({"suc_message": "success"})
    except:
        return json.dumps({"err_message": "fail to add2"})
# 一个用来加入时间文件夹的函数
def add_imagelist(file,data,name):
    imagetype=str(file.filename).split('.')[1]
    thetime=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    path='./static/image/'+name+'/'+name+'_'+thetime+'.'+imagetype
    try:
        f=open(path,'wb')
        f.write(data)
        f.close()
        return "success"
    except:
        return "fail to add"
# 通过姓名获取图片
@app.route('/get_imagebyname',methods=['POST'])
def get_imagebyname():
    name=request.values.get(u'name')
    image=open(faceDeal.getfile(name),'rb')
    resp=Response(image,mimetype='multipart/form-data')
    return resp
# 通过姓名获取图片流
@app.route('/get_imagesbyname',methods=['POST'])
def get_imagesbyname():
    name=request.values.get(u'name')
    filenamelist=faceDeal.getfiles(name)
    filelist=[]
    for i in filenamelist:
        path='./static/image/'+name+'/'+i
        image=open(path,'rb')
        filelist.append(image)
    resp=Response(filelist,mimetype='multipart/form-data')
    return resp


if __name__ == '__main__':
    app.run(debug=True)
