import base64
from PIL import Image
from io import BytesIO


def dataURIToImg(uri):
    encodedData = uri.split(',')[1]
    decodedData = base64.b64decode(encodedData)
    img = Image.open(BytesIO(decodedData))
    return img


def imgToDataURI(img):
    return base64.b64encode(img)