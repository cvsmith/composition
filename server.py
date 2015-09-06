from flask import Flask, redirect, request, url_for
import os
from werkzeug import secure_filename
import notecv.findTones as cv
import cv2
import music.music_processing as mp
from datetime import datetime
from subprocess import call
import json

UPLOAD_FOLDER = os.path.join('.', 'notecv', 'images')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


melody = Flask(__name__)
melody.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@melody.route("/", methods=['POST'])
def app():
    try:
        if request.method == 'POST':
            print dir(request)
            print 'data:{}'.format(request.data)
            image_path = save_image(request)
            image_data = do_cv(image_path)
            wav_path   = make_music(image_data)
            wav_path = url_for('static', filename='output.wav')
            return redirect(wav_path)
    except:
        import traceback,sys
        print (sys.exc_info()[0])
        traceback.print_tb(sys.exc_info()[2])

# Save image to images folder and return path to that folder
def save_image(request):
    if request.method == 'POST':
        file = request.files['file']
        name = str(datetime.now()) + '.' + file.filename
        if file and allowed_file(name):
            filename = secure_filename(name)
            path = os.path.join(melody.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            return path

def do_cv(imgPath):
    img = cv2.imread(imgPath)
    return cv.processImage(img)[0]

def make_music(imgData):
    print imgData
    currDir = os.getcwd()
    os.chdir("./music")
    # imgData = json.loads(json.dumps(imgData))
    mp.main(imgData)
    call(["mv", "./output.wav", "../static/"])
    os.chdir(currDir)
    return "./static/output.wav"

# Return True if filename is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    melody.run(host='0.0.0.0',debug=True,port=80)

