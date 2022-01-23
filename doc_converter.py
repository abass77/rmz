import numpy as np
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew
import jsonpickle
import cv2
from flask import Flask, request, Response

app = Flask(__name__)

# deskew image
def deskew_image(image):
    trace("Deskew_Image")
    image = io.imread(image)
    grayscale = rgb2gray(image)
    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, resize=True) * 255
    return rotated.astype(np.uint8)


# Check
@app.route('/check', methods=['GET'])
def check():
    output = {}
    output['status'] = "Service running"
    response_pickled = jsonpickle.encode(output)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/deskew', methods=['POST'])
def deskew():
    output = {}
    # Get destination filename
    targetfile = request.args.get("targetfile")
    # Get binary file, convert string of image data to uint8 and decode image
    data = request.data
    nparr = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image_out = deskew_image(image)
    cv2.imwrite(targetfile, image_out)
    output['status'] = "Saved"
    # Prepare response, encode JSON to return
    response_pickled = jsonpickle.encode(output)
    return Response(response=response_pickled, status=200, mimetype="application/json")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8090)