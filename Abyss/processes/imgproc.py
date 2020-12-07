
import cv2
import numpy as np
import json
import sys
import colorsys

from sklearn.cluster import KMeans

def get_dominant_color(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    clt = KMeans(n_clusters = 5)
    clt.fit(image)

    colors = clt.cluster_centers_
    hist = centroid_histogram(clt)

    maxIndex = np.argmax(hist)
    dominantColor = colors[maxIndex].astype("uint8").tolist()
    r, g, b = dominantColor[2]/255.0, dominantColor[1]/255.0, dominantColor[0]/255.0
    h, s, v = get_hsv(r, g, b)

    result = [[h, s, v], dominantColor]
    return (json.dumps(result))

def centroid_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def get_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)

    df = mx-mn

    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    
    v = mx*100
    return h, s, v