# Program to Upload Color Image and convert into Black & White image
import os
from flask import  Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)

# Open and redirect to default upload webpage
@app.route('/')
def load_form():
    return render_template('upload.html')


# Function to upload image and redirect to new webpage
@app.route('/new', methods=['POST'])
def upload_image():
    selection = request.form["image_selection"]
    file = request.files['file']
    filename = secure_filename(file.filename)
    reading_file_data = file.read()
    image_array = np.frombuffer(reading_file_data,dtype = 'uint8')
    decode_array_to_img = cv2.imdecode(image_array,cv2.IMREAD_UNCHANGED)
    if selection == "grey":
        file_data = make_grayscale(decode_array_to_img)
    elif selection == "sketch":
        file_data = image_sketch(decode_array_to_img)
    elif selection == "oil":
        file_data = oil(decode_array_to_img)
    elif selection == "rgb":
        file_data = rgb(decode_array_to_img)
    elif selection == "water":
        file_data = water_effect(decode_array_to_img)
    elif selection == "invert":
        file_data = invert(decode_array_to_img)
    elif selection == "hdr":
        file_data = hdr(decode_array_to_img)
    else:
        print("No iamge selected!!!")

   
    with open(os.path.join('static/', filename),
              'wb') as f:
        f.write(file_data)

    display_message = 'Image successfully uploaded and displayed below'
    return render_template('upload.html', filename=filename, message = display_message)



def make_grayscale(decode_array_to_img):


    # Make grayscale
    converted_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)
    status, output_image = cv2.imencode('.PNG', converted_gray_img)
    print('Status:',status)

    return output_image

def image_sketch(decode_array_to_img):
    converted_gray_img = cv2.cvtColor(decode_array_to_img,cv2.COLOR_BGR2GRAY)
    sharpening_greyimage = cv2.bitwise_not(converted_gray_img)
    blur_image = cv2.GaussianBlur(sharpening_greyimage,(111,111),0)
    sharpen_blur_image = cv2.bitwise_not(blur_image)
    sketch_image = cv2.divide(converted_gray_img,sharpen_blur_image,scale = 256.0)
    status,output_image = cv2.imencode('.PNG',sketch_image)

    return output_image

def oil(decode_array_to_img):
    rgb_image = cv2.cvtColor(decode_array_to_img,cv2.COLOR_RGBA2RGB)
    oil_effect = cv2.xphoto.oilPainting(rgb_image,7,1)
    status,output_image = cv2.imencode('.PNG',oil_effect)

    return output_image

def rgb(decode_array_to_img):
    rgb_effect_img = cv2.cvtColor(decode_array_to_img,cv2.COLOR_BGR2RGB)
    status,output_image = cv2.imencode('.PNG',rgb_effect_img)

    return output_image

def water_effect(decode_array_to_img):
    water_img = cv2.stylization(decode_array_to_img,sigma_s = 60,sigma_r = 0.6)
    status,output_image = cv2.imencode('.PNG',water_img)

    return output_image

def invert(decode_array_to_img):
    invert_img = cv2.bitwise_not(decode_array_to_img)
    status,output_image = cv2.imencode('.PNG',invert_img)

    return output_image

def hdr(decode_array_to_img):
    hdr_img = cv2.detailEnhance(decode_array_to_img,sigma_s = 12,sigma_r = 0.15)
    status,output_image = cv2.imencode('.PNG',hdr_img)

    return output_image


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename))



if __name__ == "__main__":
    app.run()


