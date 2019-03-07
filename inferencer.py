"""
Mask R-CNN
Trained on annotations found in old printed books
Copyright (c) 2018 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Jonathan Quach of BuildUCLA
------------------------------------------------------------
"""
import os
import sys
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import skimage.draw
import cv2
import requests
import urllib
from mrcnn.visualize import display_instances
from mrcnn.config import Config
from mrcnn import model as modellib, utils
from tqdm import tqdm

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
WEIGHTS_PATH_1 = "w_smallData.h5"
WEIGHTS_PATH_2 = "w_bigData.h5"

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

def detected(model, image_path=None):
    assert image_path

    # Run model detection and generate the color splash effect
    print()
    print("RUNNING ON IMAGE: {}".format(image_path))

    image = skimage.io.imread(image_path)

    # Detect objects
    r = model.detect([image], verbose=0)[0]

    if len(r['scores']) == 0:
        print('NO ROIS')
        return False
    else:
        print('ROIs FOUND WITH THE FOLLOWING SCORES:')
        for e in r['scores']:
            print(e)
        return True

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

    data = None
    if urllib.parse.urlparse(manifestURL).scheme != "":
        r = requests.get(manifestURL, verify=False)
        data = json.loads(r.content)
    else:
        with open(manifestURL, encoding='utf-8') as dataFile:
            data = json.loads(dataFile.read())
        

    imageURIs = []
    someSequence = data['sequences'][0]
    canvases = someSequence['canvases']

    for c in canvases:
        imgs = c['images']

        for i in imgs:

            resourceID = i['resource']['@id']
            potentialFileExtension = resourceID[-3:].lower()

            fileExtensions = set(['jpg', 'peg', 'png', 'iff'])
            if potentialFileExtension not in fileExtensions:
                if potentialFileExtension[-1] == '/':
                    imageURIs.append(resourceID + 'full/full/0/default.jpg')
                else:
                    imageURIs.append(resourceID + '/full/full/0/default.jpg')
            else:
                imageURIs.append(i['resource']['@id'])

    return imageURIs


def infer(manifests):
    m1, m2 = load_model(WEIGHTS_PATH_1), load_model(WEIGHTS_PATH_2)

    results = set()

    # since isImageSaved defaults to False, no splashed images are saved
    # set third argument to True to save splashed images to local directory
    imageURIs = []
    for man in manifests:
        imageURIs += getImageURIs(man)

    for img in tqdm(imageURIs):
        if detected(m1, img) or detected(m2, img):
            results.add(img)

    # create a text file that contains all image URIS of the images
    # that contain handwriting (each line contains one image URI)
    with open("regionURIs.txt", "w") as imgsFile:
        lines = sorted(results)
        imgsFile.write(lines[0])
        for img in lines[1:]:
            imgsFile.write('\n' + img)

    print("FINISHED PROCESSING MANIFESTS. SAVED regionURIS.txt TO CURRENT DIRECTORY")


def main():
    infer(sys.argv[1:])

if __name__ == '__main__':
    main()
