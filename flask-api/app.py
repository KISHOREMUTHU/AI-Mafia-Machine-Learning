import numpy as np
from numpy.core.fromnumeric import resize
import cv2
from flask import Flask
from numpy.core.records import array
from sklearn.cluster import KMeans
import urllib.request
from flask import jsonify
import json

app = Flask(__name__)
@app.route('/')
def home():
    return "Working"

@app.route('/<path:url>')
def findColors(url):

    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype = np.uint8)
    img = cv2.imdecode(arr, -1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    dominant_colors = 4
    km = KMeans(n_clusters = dominant_colors)
    all_pixels = img.reshape(img.shape[0]*img.shape[1], 3)

    km.fit(all_pixels)
    centers = km.cluster_centers_
    centers =np.array(centers,dtype ='uint8')

    i = 1
    colors = []
    for each_color in centers:
        i+=1
        colors.append(each_color)
        # color swatch
        a = np.zeros((100,100,3), dtype ='uint8')
        a[:,:,:] = each_color

    print(colors)

    return jsonify(
        colors = json.dumps(np.array(colors).tolist(), default=str)
    )

if __name__ == '__main__':
    app.run(debug=True) 