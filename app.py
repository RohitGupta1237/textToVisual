from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from google_images_download import google_images_download

import os
import shutil

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/visual', methods=['POST'])
def visual():
   name = request.form.get('name')
   object = request.form.get('object')

   path = './downloads/' + object
   destpath = './static/' + object
   if not os.path.exists(path):
        response = google_images_download.googleimagesdownload();
        arguments = {"keywords": object, "limit": 10, "print_urls": True}
        paths = response.download(arguments)

   if not os.path.exists(destpath):
        shutil.copytree(path, destpath)

   imgPaths = ["", "", "", "", "", "", "", "", "", ""]
   i = 0

   newpath = './../downloads/' + object

   for filename in os.listdir(path):
        imgPaths[i] = object +'/'+filename
        i = i + 1
   if name:
       print('Request for visual page received with name=%s' % name)

       return render_template('visual.html', name = name, object=object, images=imgPaths)
   else:
       print('Request for visual page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()