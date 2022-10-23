from io import BytesIO
from typing import cast
from flask import Flask, request, send_file
from flask_cors import CORS
import cv2
import numpy as np
from numpy import ndarray
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
cors = CORS(app)


@app.route("/apply_filter", methods=["POST"])
def apply_filter():
  input_image = request.files['image']
  img = cv2.imdecode(np.asarray(bytearray(input_image.stream.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
  filter_type = request.form.get('filter_type').lower()

  if filter_type == 'gaussian_blur':
    pass
  elif filter_type == 'greyscale':
    pass
  elif filter_type == 'invert':
    kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
    channel_ndarray: ndarray = cv2.filter2D(img, -1, kernel)
  else:
    return

  # channel_ndarray should be 3 channel
  encoded, plain_ndarray = cv2.imencode('.png', channel_ndarray)
  encoded, plain_ndarray = cast(tuple[bool, ndarray], (encoded, plain_ndarray))
  return send_file(BytesIO(plain_ndarray.tobytes()), mimetype='image/gif')


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
