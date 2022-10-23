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
  img: ndarray = cv2.imdecode(np.asarray(bytearray(input_image.stream.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
  filter_type = request.form.get('filter_type').lower()
  amount_str = request.form.get('amount')
  amount = int(amount_str) if amount_str != None else 1
  print(f'{img.shape}')

  if filter_type == 'gaussian_blur':
    pass
  elif filter_type == 'grayscale':
    # channel_ndarray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    channel_ndarray = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
  elif filter_type == 'sharpen':
    basic_kernel = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    sharpen_kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]) * amount
    kernel = basic_kernel + sharpen_kernel
    channel_ndarray: ndarray = cv2.filter2D(img, -1, kernel)
  else:
    return

  print(f'{channel_ndarray.shape}')
  # channel_ndarray should be 3 channel
  encoded, plain_ndarray = cv2.imencode('.png', channel_ndarray)
  encoded, plain_ndarray = cast(tuple[bool, ndarray], (encoded, plain_ndarray))
  return send_file(BytesIO(plain_ndarray.tobytes()), mimetype='image/gif', download_name='out.png')


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
