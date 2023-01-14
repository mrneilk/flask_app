from flask import Flask,render_template,redirect,request,send_from_directory
from tensorflow.keras.models import load_model
import os
from PIL import Image
import numpy as np
from werkzeug.utils import secure_filename

model_file = "model4.h5"
model = load_model(model_file)

app = Flask(__name__,template_folder='template')
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

def makePredictions(path,color=True):
    '''
    Method to predict if the image uploaed is healthy or pneumonic
    '''
    image = Image.open(path) 
# we open the image
#   img_d = img.resize((224,224))
#   # we resize the image for the model
#   rgbimg=None
#   #We check if image is RGB or not
#   if len(np.array(img_d).shape)<3:
#     rgbimg = Image.new("RGB", img_d.size)
#     rgbimg.paste(img_d)
#   else:
#       rgbimg = img_d
#   rgbimg = np.array(rgbimg,dtype=np.float64)
#   rgbimg = rgbimg.reshape((1,64,64,3))
#   predictions = model.predict(rgbimg)
#   a = int(np.argmax(predictions))
    if color:
            image = image.convert("RGB")
        # plt.imshow(np.asarray(image))
    data = np.array(image.resize((64,64), Image.ANTIALIAS)).reshape(1, 64, 64, 3 if color else 1)/255

    if model.predict(data) > 0.5:
        return "Pneumonic"
    else:
        return "Healthy"
    # return a

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        if 'img' not in request.files:
            return render_template('home.html',filename="lungs.jpg",message="Please upload an file")
        f = request.files['img'] 
        filename = secure_filename(f.filename) 
        if f.filename=='':
            return render_template('home.html',filename="lungs.jpg",message="No file selected")
        if not ('jpeg' in f.filename or 'png' in f.filename or 'jpg' in f.filename):
            return render_template('home.html',filename="lungs.jpg",message="please upload an image with .png or .jpg/.jpeg extension")
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        if len(files)==1:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        else:
            files.remove("lungs.jpg")
            file_ = files[0]
            os.remove(app.config['UPLOAD_FOLDER']+'/'+file_)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        predictions = makePredictions(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return render_template('home.html',filename=f.filename,message=predictions,show=True)
    return render_template('home.html',filename='lungs.jpg')

@app.route('/abouttool.html',methods=['GET','POST'])
def f1():
     return render_template('abouttool.html')

@app.route('/pneumonia.html',methods=['GET','POST'])
def f2():
     return render_template('pneumonia.html')

if __name__=="__main__":
    app.run(debug=True)