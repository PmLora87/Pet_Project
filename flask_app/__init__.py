from flask import Flask
import os

app = Flask(__name__)

app.secret_key = "Baaaark"
# specify path to folder where you want to save uploads
app.config['UPLOAD_FOLDER'] = "static/images/"
# specify the max size of post requests (image file upload limits in this case)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024