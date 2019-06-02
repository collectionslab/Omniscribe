# Omniscribe

[![DOI](https://zenodo.org/badge/114576206.svg)](https://zenodo.org/badge/latestdoi/114576206)

Omniscribe was developed to detect annotations (margnialia, interlinear markings, provenance marks, etc.) in digitized printed books hosted via the International Image Interoperability Framework (IIIF). Why do we care about finding annotations? Annotations and other marks are traces left behind by previous readers and owners. Through these markings, we can better understand how readers in the past have used their books or interpreted their contents.

Formed in December 2018, the project is a Collections Lab/BuildUCLA collaboration with a team of UCLA Digital Library staff and UCLA students.

#### Phase 2 Project team: train model and develop application
* Dawn Childress, project lead
* Jonathan Quach, Mask-RCNN model and app development
* Morgan Madjukie, app development 
* Pete Broadwell, consultant
* Andrew Wallace, consultant

#### Phase 1 Project team: research and testing
* Dawn Childress
* Pete Broadwell
* Johnny Ho
* Andrew Wallace
* Jonathan Quach
* Morgan Madjukie
* Emily Chen
* Rahul Malavalli

![annotations.png](sample.png)

**Fig. 1 A sample image generated using our Mask-RCNN model.**

### Data

Thank you for using Omniscribe! **inferencer.py** implements the command-line interface for users, but does require pre-trained weights as produced by Mask R-CNN.

## Files (Requires Python 3.6.x)

### inferencer.py

This script is the engine that does all the handwriting detection. It currently takes a list of manifests via command line and will save all images referred by the manifest that it predicts has at least one region that contains handwriting.

The script will display information of its configuration for Mask R-CNN, the weights of the models it will use to infer, the manifest URI it is currently running on, the image URI it is currently inferring on, and confidence scores in range [0.96, 1] of any region it picks up (the higher the score, the more confident the model believes a region contains handwriting).

$ python3 inferencer.py https://marinus.library.ucla.edu/iiif/annotated/uclaclark_SB322S53.json https://marinus.library.ucla.edu/iiif/annotated/uclaclark_BF1681A441713.json

### exportFiles.py

A utility script that **inferencer.py** imports to allow for exporting the results in HTML format and manifest (JSON) format.

## UPDATE #2 February 13, 2019

#### mask-rcnn/

This is the vanilla Mask-RCNN that is re-purposed for detecting annotations. For more information, please refer to <https://github.com/matterport/Mask_RCNN>.

### requirements.txt

A list of dependencies needed to run this package. To be used as follows:

$ pip3 install -r requirements.txt

### model.h5

This is the weights file that implements the model that does the inferencing. It can be downloaded from the
[releases]|(https://github.com/collectionslab/Omniscribe/releases) page and should be saved into the root folder
of the project.

There are various ways that we can evaluate these models. Ideally, we would have these models see a test set, know the total amount of annotated regions in this test set, and perhaps compute an F1 score and an accuracy score. However, what makes something a "region" for us is arguably blurred. For example, when considering a whole page of handwriting, *m*<sub>small</sub> would detect multiple regions, stratisfying the page. *m*<sub>zoo</sub> however, would see the entire page as one region of annotation. Both models are correct, but accuracy score would not account for the difference in their predictions. We also should not use F1 because there are uncountably many regions that are not annotated, which makes for an indefinite amount of True Negatives in the F1 calculation. For now, we have settled on using a True Positive / False Positive ratio (TP/FP) as a metric of evaluation. That is, the higher the TP/FP, the better a model is performing.

In our test set, *m*<sub>small</sub> scored a TP/FP of 140/14, while *m*<sub>zoo</sub> received a higher TP/FP of 87/7. However, a qualitative anaylsis suggests that neither of these models should be used alone. We found that *m*<sub>small</sub> detected interlinear annotations and rarely detected tiny annotations (e.g. a lone # or a scribbled number), while *m*<sub>zoo</sub> detected tiny annotations but never found interlinear annotations. At this point, we have made the decision to allow both models to observe an image, and further process the image should either model detect at least one region in it.

We are also now looking to wrap up these models in a nice package for others to use. The plan is to integrate Flask with our machine learning tools to achieve the goal of usability. In the meantime, we are also planning to upload more of our data onto Zooniverse so that we can later train a third model that may improve on our current choice of having two models.
___

## UPDATE #1 January 3, 2019

🎉Happy New Year!🎉

The team had one meeting over winter break.  We discussed possible pipelines
for integrating IIIF manifests as input for our tool.

As of now, our tool has a command-line interface, taking local images as input
and outputting a copy of the image with a color spash on any annotation found;
however, a large collection of annotated books are actually archived over IIIF
servers. With this in mind, we are looking into porting this tool to a web
interface that can instead retrieve annotations from IIIF manifests.

___

## Approaches we explored during Phase 1

* Mask-RCNN (current approach)

* Auto-Keras

**Mask-RCNN** is currently our best solution to detecting annotations. It is
state-of-the-art in computer vision as it is the result of continuous
advancements in using convolutional neural networks for **image segmentation**.
More information of its upbringing as well as its predecessors are found below.

<https://arxiv.org/pdf/1703.06870.pdf>
<https://github.com/matterport/Mask_RCNN>

Perhaps what makes Mask-RCNN the most feasible solution for us over other
approaches is the fact that we can treat our images as regions and consider
annotations as **regions of interest** (ROIs). This is in contrast of treating
our problem as a binary classification problem (i.e. annotated v.s. not
annotated). After training the Mask-RCNN on our dataset, we get desirable
results as shown in **Figure 1**.

___

**Auto-Keras** is currently the best open-source library for automatically
generating machine learning models for your datasets. It competes directly with
Google's AutoML and has an active community backing it. More information can
be found in the link below.

<https://autokeras.com>

From our experience, we believe that Auto-Keras is a great tool for those who
want to do simple image classification. However, we found that the models
they generate are generally dense and complex to achieve desirable results
where a simpler model with fewer layers will perform just as well or even
better. For the more experienced, we recommend using the models that Auto-Keras
generates as benchmarks for your own models. It is also important to note that
only image classification is supported as of 1/3/19, with ML features for text,
audio, and video as possible features as the community grows larger to
implement them.

## Approaches we Have Attempted During December 2017 - June 2018

* Vanilla CNN (implemented in PyTorch)

* PyTesseract

* OpenCV

The following link discusses our experience with the approaches aforementioned,
including project overview, data preparation, data pre-processing, and
comparing non-ML v.s. ML approaches.

<https://docs.google.com/presentation/d/1rqTioMwiLpMBgRY8NdbcbXLtifYfNxk7ZT2d6d3Yyes/edit#slide=id.g353a76bac2_0_525>