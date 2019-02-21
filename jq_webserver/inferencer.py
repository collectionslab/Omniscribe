"""
Mask R-CNN
Trained on annotations found in old printed books
Copyright (c) 2018 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Jonathan Quach of BuildUCLA
------------------------------------------------------------
"""

import sys
import os
import sys
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import skimage.draw
import cv2
import requests
from mrcnn.visualize import display_instances
from mrcnn.config import Config
from mrcnn import model as modellib, utils

# frowned upon because of security breaches but needed to connect to manifests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# Root directory of the project
ROOT_DIR = os.path.abspath("../../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library


# Directory to save logs and model checkpoints; necessary to run mrcnn modules
DEFAULT_LOGS_DIR = "logs/"

# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
WEIGHTS_PATH_1 = "weights/smallData_0007.h5"
WEIGHTS_PATH_2 = "weights/zooniverse_0014.h5"

############################################################
#  Configurations
############################################################


class CustomConfig(Config):
    # Give the configuration a recognizable name
    NAME = "handwriting"

    # faster to train than using resnet101 as backbone
    BACKBONE = "resnet50"

    # We use a GPU with 8GB memory, which usually fits 2 images
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 2

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + handwriting

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 50

    # Skip detections with < 96% confidence
    DETECTION_MIN_CONFIDENCE = 0.96


def color_splash(image, mask):
    gray = skimage.color.gray2rgb(skimage.color.rgb2gray(image)) * 255
    mask = (np.sum(mask, -1, keepdims=True) >= 1)
    if mask.shape[0] > 0:
        splash = np.where(mask, image, gray).astype(np.uint8)
    else:
        splash = gray
    return splash


def detect_and_color_splash(model, image_path=None, isImageSaved=False):
    assert image_path

    # Run model detection and generate the color splash effect
    print("RUNNING ON IMAGE: {}".format(image_path))

    image = skimage.io.imread(image_path)

    # Detect objects
    r = model.detect([image], verbose=0)[0]

    if len(r['scores']) == 0:
        print('NO ROIS')
        return None
    else:
        print('ROIs FOUND WITH THE FOLLOWING SCORES:')
        for e in r['scores']:
            print(e)

        if isImageSaved:
            # using part of the image_path as an identifier
            # endIndex = image_path[:image_path.rindex('.')].rindex('.')
            # fileName = image_path[image_path.index('_'):endIndex]

            # Save splashed image to a directory called detectedImages
            splash = color_splash(image, r['masks'])
            # file_name = "detectedImages/{}.png".format(fileName)
            file_name = "splash_{:%Y%m%dT%H%M%S}.png".format(datetime.datetime.now())
            skimage.io.imsave(file_name, splash)
            print("IMAGE IS SAVED TO ", file_name)
        return image_path

############################################################
#  Load a trained model
############################################################


def load_model(weights_path):
    assert weights_path

    class InferenceConfig(CustomConfig):

        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

    config = InferenceConfig()

    model = modellib.MaskRCNN(mode="inference", config=config,
                              model_dir=DEFAULT_LOGS_DIR)

    # Load weights
    print("LOADING WEIGHTS: ", weights_path)
    model.load_weights(weights_path, by_name=True)

    return model


def getImageURIs(manifestURL=None):
    url = manifestURL
    r = requests.get(url, verify=False)
    data = json.loads(r.content)

    imageURIs = []
    someSequence = data['sequences'][0]
    canvases = someSequence['canvases']

    for c in canvases:
        imgs = c['images']

        for i in imgs:

            resourceID = i['resource']['@id']
            potentialFileExtension = resourceID[-3:].lower()

            fileExtensions = set(['jpg','peg','png','iff'])
            if potentialFileExtension not in fileExtensions:
                if potentialFileExtension[-1] == '/':
                    imageURIs.append(resourceID + 'full/full/0/default.jpg')
                else:
                    imageURIs.append(resourceID + '/full/full/0/default.jpg')
            else:
                imageURIs.append(i['resource']['@id'])

    return imageURIs


def detect_annotations_from_manifest(model, manifest_path, isImageSaved=False):
    assert model and manifest_path

    annotatedPages = set()
    imageURIs = getImageURIs(manifest_path)

    print('LOOKING INTO THIS MANIFEST: ', manifest_path)
    print('INFERENCING WITH THIS MODEL: ', model)

    for img in imageURIs:
        prediction = detect_and_color_splash(model, img, isImageSaved)
        if prediction is not None:
            annotatedPages.add(img)

    return annotatedPages


def infer(manifests):
    m1, m2 = load_model(WEIGHTS_PATH_1), load_model(WEIGHTS_PATH_2)

    results = set()

    # since isImageSaved defaults to False, no splashed images are saved
    # set third argument to True to save splashed images to local directory
    for man in manifests:
        results = results.union(detect_annotations_from_manifest(m1, man))
        results = results.union(detect_annotations_from_manifest(m2, man))

    # create a text file that contains all image URIS of the images
    # that contain handwriting (each line contains one image URI)
    with open("regionURIs.txt", "w") as imgsFile:
        lines = sorted(results)
        imgsFile.write(lines[0])
        for img in lines[1:]:
            imgsFile.write('\n' + img)

    return sorted(results)