"""
General utility functions
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plt_img(img, rois=None, roi_level_set=set([1,2,3,4,5]),
            figsize=(8,6), dpi=200,
           ):
    """
    Plot the image and ROIs (if they are provided).
    See https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image
    
    :params rois: a list of tuple: a list of ImageROIs coupled with the roi edge color, e.g., [(img_roi_ground_truth,'b')]
    :params roi_level: only print the ROIs boxes that have the level in this set parameter. Level:
                       block(2), para(3), textline(4), word(5)  
    """
    # create figure and axes
    fig, ax = plt.subplots(1, figsize=figsize, dpi=dpi)
   
    # display the image
    plt.imshow(img, cmap='gray')
    
    # create bounding box if there is
    count = 0
    if rois is not None:
        for rois_, edgecolor in rois:
            for idx, roi in enumerate(rois_):
                rect = patches.Rectangle((roi.x,roi.y),roi.width, roi.height,
                                         linewidth=2,
                                         edgecolor=edgecolor,
                                         facecolor='none')

                # check if the level of the roi is in the set
                if roi.level in roi_level_set:
                    ax.add_patch(rect)
                    print(roi.toString())
                    count+=1
                
    print("Number of ROIs plotted: %s"%count)


def save_rois(imgROIs, fpath):
    """
    Save the image rois into a txt file
    """
    with open(fpath,"w") as f:
        for roi in imgROIs:
            f.write('%s\n' %roi.toString())
    

























