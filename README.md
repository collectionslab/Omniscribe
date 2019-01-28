# Book Annotation Detection Engine

## Collections Lab Team

Formed in December 2018, the project is a Collections Lab/BuildUCLA collaboration with a team consisting of UCLA library staff and students based in the UCLA Digital Library Program.

### Objective

Develop software that detects annotations in historical printed books that are
stored in International Image Interoperability Framework (IIIF) servers.

![annotations.png](sample.png)
**Fig. 1 A sample image generated from using Mask-RCNN.**

This tool will automate the process of sifting through every page manually to
retrieve annotations, thus being useful for scholars who are interested in
active reading or even the annotations themselves.

## Data

<https://ucla.app.box.com/folder/45481483089>

### Project team

* Dawn Childress (project lead, 12/17- )
* Pete Broadwell (12/17-12/18)
* Andrew Wallace (12/17- )
* Jonathan Quach (12/17- )
* Morgan Madjukie (12/17- )
* Johnny Ho (12/17-06/18)
* Emily Chen (12/17-06/18)
* Rahul Malavalli (12/17-06/18)

### More Info on Some Files in this Path

.gitignore

Intentionally not track pycache .pyc and .ipynb_checkpoints since they do not
provide convenient information about changes that may have occured to the code.

preproc.py

Binarizes an image or a folder of images (NOTE: must provide an output
path if binarizing an entire folder)

E.g.

$ python preproc.py img.png #this is for one image

$ python preproc.py --out /Users/John/Desktop/outputFolder /Users/John/Desktop/inputFolder

sampler.py

Randomly generates "number" square subsamples of side length "px" from
file(s) "files" where "number" "px" and "files" are from user input.

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

### Current TODO

1. Attend IIIF workshop hosted by our very own **Dawn Childress** and learn how to use IIIF API.

2. Establish a pipeline to integrate IIIF with our tool.

## Approaches we Have Attempted During July 2018 - August 2018

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
