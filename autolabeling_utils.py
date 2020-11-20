import os
from datetime import datetime
import io
from PIL import Image
import base64
import json

from util_path import path_list

def checkdir(dirpath, create=False):
    result = os.path.isdir(dirpath)
    if create and not result:
        os.makedirs(dirpath)
    return result


def now_name():
    return datetime.now().strftime('%Y%m%d%H%M')


def detail_now_name():
    return datetime.now().strftime('%Y%m%d%H%M%f')


def create_circle_labelme_json(pos, radius, filename, height, width, frame):

    # pngBIO = io.BytesIO()
    # image = Image.fromarray(frame)
    # image.save(pngBIO, format='png')
    # b_frame = pngBIO.getvalue()

    points = [
        [float(pos[0]), float(pos[1])],
        [float(pos[0]) + float(radius), float(pos[1])],
    ]

    shapes = []
    shape = {}
    shape["label"] = "pov"
    shape["points"] = points
    shape["group_id"] = None
    shape["shape_type"] = "circle"
    shape["flags"] = {}
    shapes.append(shape)

    json_data = {}

    json_data["version"] = "4.5.5"
    json_data["flags"] = {}
    json_data["shapes"] = shapes
    json_data["imagePath"] = filename
    # json_data["imageData"] = base64.b64encode(b_frame).decode('utf-8')
    json_data["imageData"] = ''
    json_data["imageHeight"] = height
    json_data["imageWidth"] = width

    return json_data


def convert_valid_json_data(dirpath):
    jsonpath_list = path_list(dirpath, pattern='*.json')
    for jsonpath in jsonpath_list:
        with open(jsonpath, 'r') as f:
            json_data = json.load(f)

        image_name = json_data['imagePath']
        image_path = os.path.join(os.path.dirname(jsonpath), image_name)
        with open(image_path, 'rb') as f:
            bdata = f.read()
        img_data = base64.b64encode(bdata).decode('utf-8')
        json_data['imageData'] = img_data
        with open(jsonpath, "w") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
