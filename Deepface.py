import argparse
import time
import uuid

from deepface import DeepFace
from flask import Flask, request, jsonify
from imread_from_url import imread_from_url
from retinaface import RetinaFace

from yolov7 import YOLOv7, utils

app = Flask(__name__)


# ------------------------------
# Service API Interface


@app.route('/')
def index():
    return '<h1>Hello, deepface!</h1>'


@app.route('/analyze', methods=['POST'])
def analyze():
    tic = time.time()
    req = request.get_json()
    trx_id = uuid.uuid4()

    # ---------------------------
    resp_obj = analyzeWrapper(req)

    # ---------------------------

    toc = time.time()

    resp_obj["trx_id"] = trx_id
    resp_obj["seconds"] = toc - tic

    return resp_obj


def analyzeWrapper(req):
    instances = []
    if "img" in list(req.keys()):
        raw_content = req["img"]  # list

        for item in raw_content:  # item is in type of dict
            instances.append(item)

    if len(instances) == 0:
        return jsonify({'success': False, 'error': 'you must pass at least one img object in your request'}), 205

    print("Analyzing ", len(instances), " instances")

    actions = ['emotion', 'age', 'gender', 'race']

    if "actions" in list(req.keys()):
        actions = req["actions"]
    results = DeepFace.analyze(instances[0], actions=actions, enforce_detection=False,
                               detector_backend="retinaface")
    i = 1
    resp_obj = {}
    for result in results:
        resp_obj["instance_" + str(i)] = result
        i = i + 1
    return resp_obj


@app.route('/verify', methods=['POST'])
def verify():
    tic = time.time()
    req = request.get_json()
    trx_id = uuid.uuid4()

    resp_obj = jsonify({'success': False})
    resp_obj = verifyWrapper(req, trx_id)

    # --------------------------

    toc = time.time()

    resp_obj["trx_id"] = trx_id
    resp_obj["seconds"] = toc - tic

    return resp_obj, 200


def verifyWrapper(req, trx_id=0):
    resp_obj = jsonify({'success': False})

    model_name = "VGG-Face";
    distance_metric = "cosine";
    detector_backend = "opencv"
    if "model_name" in list(req.keys()):
        model_name = req["model_name"]
    if "distance_metric" in list(req.keys()):
        distance_metric = req["distance_metric"]
    if "detector_backend" in list(req.keys()):
        detector_backend = req["detector_backend"]

    # ----------------------

    instances = []
    if "img" in list(req.keys()):
        raw_content = req["img"]  # list

        for item in raw_content:  # item is in type of dict
            instance = []
            img1 = item["img1"];
            img2 = item["img2"]

            validate_img1 = False
            if len(img1) > 11 and img1[0:11] == "data:image/":
                validate_img1 = True

            validate_img2 = False
            if len(img2) > 11 and img2[0:11] == "data:image/":
                validate_img2 = True

            if validate_img1 != True or validate_img2 != True:
                return jsonify(
                    {'success': False, 'error': 'you must pass both img1 and img2 as base64 encoded string'}), 205

            instance.append(img1);
            instance.append(img2)
            instances.append(instance)

    # --------------------------

    if len(instances) == 0:
        return jsonify({'success': False, 'error': 'you must pass at least one img object in your request'}), 205

    print("Input request of ", trx_id, " has ", len(instances), " pairs to verify")

    # --------------------------

    try:
        resp_obj = DeepFace.verify(instances
                                   , model_name=model_name
                                   , distance_metric=distance_metric
                                   , detector_backend=detector_backend
                                   )

        if model_name == "Ensemble":  # issue 198.
            for key in resp_obj:  # issue 198.
                resp_obj[key]['verified'] = bool(resp_obj[key]['verified'])

    except Exception as err:
        resp_obj = jsonify({'success': False, 'error': str(err)}), 205

    return resp_obj


@app.route('/represent', methods=['POST'])
def represent():
    tic = time.time()
    req = request.get_json()
    trx_id = uuid.uuid4()

    resp_obj = jsonify({'success': False})
    resp_obj = representWrapper(req, trx_id)

    # --------------------------

    toc = time.time()

    resp_obj["trx_id"] = trx_id
    resp_obj["seconds"] = toc - tic

    return resp_obj, 200


@app.route('/persons', methods=["POST"])
def persons():
    if request.method != "POST":
        return
    instances = request.get_json()['img']
    results = []
    if instances and len(instances) > 0:
        for instance in instances:
            boxes, scores, class_ids = yolov7_detector(instance)
            output = utils.format_output(boxes, scores, class_ids)
            count_persons = sum(1 for item in output if item.get('name') == 'person')
            results.append(count_persons)
    return results


@app.route('/objects', methods=["POST"])
def objects():
    if request.method != "POST":
        return
    instances = request.get_json()['img']
    results = []
    if instances and len(instances) > 0:
        for instance in instances:
            boxes, scores, class_ids = yolov7_detector(instance)
            results.append(utils.format_output(boxes, scores, class_ids))
    return results


def representWrapper(req, trx_id=0):
    resp_obj = jsonify({'success': False})

    # -------------------------------------
    # find out model

    model_name = "VGG-Face";
    distance_metric = "cosine";
    detector_backend = 'opencv'

    if "model_name" in list(req.keys()):
        model_name = req["model_name"]

    if "detector_backend" in list(req.keys()):
        detector_backend = req["detector_backend"]

    # -------------------------------------
    # retrieve images from request

    img = ""
    if "img" in list(req.keys()):
        img = req["img"]  # list
    # print("img: ", img)

    validate_img = False
    if len(img) > 11 and img[0:11] == "data:image/":
        validate_img = True

    if validate_img != True:
        print("invalid image passed!")
        return jsonify({'success': False, 'error': 'you must pass img as base64 encoded string'}), 205

    # -------------------------------------
    # call represent function from the interface

    try:

        embedding = DeepFace.represent(img
                                       , model_name=model_name
                                       , detector_backend=detector_backend
                                       )

    except Exception as err:
        print("Exception: ", str(err))
        resp_obj = jsonify({'success': False, 'error': str(err)}), 205

    # -------------------------------------

    # print("embedding is ", len(embedding)," dimensional vector")
    resp_obj = {}
    resp_obj["embedding"] = embedding

    # -------------------------------------

    return resp_obj


if __name__ == "__main__":
    print("人脸识别v2.0.0")
    DeepFace.build_model("Race")
    DeepFace.build_model("Age")
    DeepFace.build_model("Gender")
    DeepFace.build_model("Emotion")
    RetinaFace.build_model()
    yolov7_detector = YOLOv7("yolov5s.onnx", conf_thres=0.2, iou_thres=0.3)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=1234,
        help='Port of serving api')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)
