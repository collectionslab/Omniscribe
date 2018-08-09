Docs
==== 

image_label_generator.py

This is an event-handled GUI that allows the user to label images into
binary classifications using the left and right arrow keys (where pressing left
on an image will send it to a folder that is intended to be for positive images
and pressing right will send it to a folder for negative images). 

Using the -c flag will consider the image as is to be labeled on the grounds
that the image is considered pre-cropped. Omitting the -c flag will generate
a cropped version of the image where the crop comes from a csv file that
presumably contains the pixel length, pixel width, x-coordinate, and 
y-coordinate.


-i, --input  | 'input directory')
-p, --positive | 'directory where positive image samples should be output'
-n, --negative | 'directory where negative image samples should be output')
-c, --cropped, | 'if set, tells the generator to assume images are precropped.'

E.g.

$ python image_label_generator.py --input folder/of/all/images -c --positive folder/with/positive/images --negative folder/with/negative/images


image_sample_generator.py

This script has one function: Generate and save random subsamples of an image.
    
    Required Parameters:
        - input file or directory
        - output directory
        - output image sizes, in format xsize,ysize
        
    Optional Parameters:
        - stride, in format xstride,ystride
            - if stride is uninitialized, it will be default to 1 pixel 
        - number of output images. if not set, it defaults to all the images




E.g. 

The commands below generate the same results, producing all subsample images
that fit in a 28 x 28 window with a stride step of 1 pixel

$ python image_label_generator.py --input folder/of/some/images --output folder/of/subsampled/images --dimensions 28
$ python image_label_generator.py --input folder/of/some/images --output folder/of/subsampled/images --dimensions 28 28 



This command generates all subsample images of width 128 pixels and height 56 pixels at a stride step of 2

$ python image_label_generator.py --input folder/of/some/images --output folder/of/subsampled/images --dimensions 128 56 --stride 2

This command generates only 100 subsample images of width 128 pixels and height 56 pixels at a stride step of 2

$ python image_label_generator.py --input folder/of/some/images --output folder/of/subsampled/images --dimensions 128 56 --stride 2 --number 100
