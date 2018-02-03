# Meeting agendas

## 01/11/18
- Go through some ML background:
  - [Andrew's Ng tutorial](https://www.coursera.org/learn/machine-learning)
  - [pytorch CIFAR tutorial](http://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)

## 01/18/18
- Discuss about last week ML materials
- [Sample data](https://calisphere.org/item/7334deb2-fbf2-4af8-9643-23e8ae1225d9/?order=44)
- [Raw data: the annotated books image set (first 10 books only)](http://babylon.library.ucla.edu/~broadwell/clark_annotated/)
- Go through [Tesseract](https://github.com/madmaze/pytesseract)
- Develop a simple ML model on recognizing handwriting text on images, including:
  - doing text recognition using tesseract
  - opened-minded
- Read research paper

## 01/25/18
- Go through Peter's suggested [article](https://blogs.dropbox.com/tech/2017/04/creating-a-modern-ocr-pipeline-using-computer-vision-and-deep-learning/)
- Weekly meeting: Aigle style - go back implement soln, come back discuss, go back implement soln, [loop]
  - Goal: everyweek makes progress
- Data labeling: [Amazon mTurk?](https://www.mturk.com/)
  - Goal: Get a set of >10k labeled images (printed / printed + written)
- GAN to generate synthetic imaging data (printed or printed + written); RCNN for text object detection
  - Goal: Explore the feasibility of GAN to generate synthetic data, the behavior of GAN in this type of data. Can GAN generate different font text?
  - Goal: can we use RCNN to identify text objects in a page? Or can we do something else?
- Tessearct
  - Build the text classification pipeline: load data, preprocessing, tesseract classification
  - Goal: how well Tessearct in text reconigition on our dataset? Can it identify written text? Can we improve printed text classification?
- Naive CNN approach
  - Goal: how good naive CNN can classify labeled images? What about images with different fonts and styles? What about multi-box classification (majority vote)?
- Research
  - Goal: What's the state of the art method for printed vs written text classification research?
- Data, web workstation
  - Goal: create a dataset
- *Note: My suggestion is only for guidance. The ultimate solution is created together (Does not have to follow my suggestions).*  

## 02/2/18
-Uploaded labeled dataset of our initial 10 manuscripts.
 -Dataset consists of an annotated (+) folder, unannotated (-) folder, and a README abou edge cases of classification
  -1977 annotated, 842 unannotated ~1.6gb


