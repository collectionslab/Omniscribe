# Book Annotation Classification Engine

A UCLA Collections Lab/BuildUCLA project: computer vision experiments to identify and classify annotations in digitized printed books in IIIF-hosted collections.

Status: Experimenting with different neural network architectures and evaluating their performances on a dataset of over 3000 images. 

Want to help us build our training data? Tag and classify annotation here: https://www.zooniverse.org/projects/kirschbombe/book-annotation-classification

## Data
https://ucla.app.box.com/folder/45481483089

### Project team

* Dawn Childress
* Pete Broadwell
* Andrew Wallace
* Johnny Ho
* Emily Chen
* Jonathan Quach
* Morgan Madjukie
* Rahul Malavalli


### More Info on Some Files in this Path

.gitignore

Intentionally not track pycache .pyc and .ipynb_checkpoints since they do not
provide convenient information about changes that may have occured to the code.

__init__.py

Standard file to be included to treat folders as packages (list of modules)
so as to allow modularization

preproc.py

Binarizes an image or a folder of images (NOTE: must provide an output 
path if binarizing an entire folder) 

E.g. 

$ python preproc.py img.png #one image
$ python preproc.py --out /Users/John/Desktop/outputFolder /Users/John/Desktop/inputFolder


sampler.py

Randomly generates "number" square subsamples of side length "px" from
file(s) "files" where "number" "px" and "files" are from user input.
