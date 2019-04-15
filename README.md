# Omniscribe

Thank you for using Omniscribe! **inferencer.py** implements the command-line interface for users, but does require pre-trained weights as produced by Mask R-CNN.

## Files (Requires Python 3.6+)

### inferencer.py

This script is the engine that does all the handwriting detection. It currently takes a list of manifests via command line and will save all images referred by the manifest that it predicts has at least one region that contains handwriting.

The script will display information of its configuration for Mask R-CNN, the weights of the models it will use to infer, the manifest URI it is currently running on, the image URI it is currently inferring on, and confidence scores in range [0.96, 1] of any region it picks up (the higher the score, the more confident the model believes a region contains handwriting).

$ python3 inferencer.py https://marinus.library.ucla.edu/iiif/annotated/uclaclark_SB322S53.json https://marinus.library.ucla.edu/iiif/annotated/uclaclark_BF1681A441713.json

### exportFiles.py

A utility script that **inferencer.py** imports to allow for exporting the results in HTML format and manifest (JSON) format.

#### mask-rcnn/

This is the vanilla Mask-RCNN that is re-purposed for detecting annotations. For more information, please refer to <https://github.com/matterport/Mask_RCNN>.

### requirements.txt

A list of dependencies needed to run this package. To be used as follows:

$ pip3 install -r requirements.txt

### model.h5 (not shown here)

This is the the weights file that implements the model that does the inferencing.