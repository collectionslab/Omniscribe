"""
To be used on the csv file generated from zooniverse
Currently assumes the zooniverse data and meta data of our annotations are in the same directory as this script
"""

import pandas as pd
import json

CSV_PATH = "rawData.csv"

# WARNING CSV file is inconsistent with the key identifier for the key names. "filename" and "0001_R.png" are valid key names
def extractROIs(csv_file_path):
    assert csv_file_path
    df = pd.read_csv(csv_file_path, usecols=["annotations", "subject_data","subject_ids"])

    fileNames = []
    coordinates = []

    # gets all fileNames of images in rows that use "filename" as the key
    for index, row in df.iterrows():

        s_id = str(row["subject_ids"])

        s_data = json.loads(row["subject_data"])

        # 
        fn = None
        try: # if this succeeds, then we can retrieve its annotations as well
            fn = s_data[s_id]["filename"]
        except:
            try:
                fn = s_data[s_id]["uclaclark_Q143B7S3_0121.png"]
            except:
                    fn = s_data[s_id]["0001_R.png"]

        fileNames.append(fn)
        
        tasks = json.loads(df.iloc[index]["annotations"])

        imageCoordinates = []

        for t in tasks:

            if t["task"] == "T1" or t["task"] == "T4":
                listOfCoordinates = t["value"]

                for coord in listOfCoordinates:
                    formattedCoord = int(coord["x"]), int(coord["y"]), int(coord["width"]), int(coord["height"])
                    imageCoordinates.append(formattedCoord)

        coordinates.append(imageCoordinates)

    duplicatedRegionData = list(zip(fileNames,coordinates))

    d = dict()

    # Some of the annotations that zooniverse users made did not fit with our definition of an annotation (e.g. a stray mark)
    falsePositives = []

    region_count = 0
    for pair in duplicatedRegionData:

        # skin unannotated regions
        if pair[0] in falsePositives or not pair[1]:
            continue

        if pair[0] in d:
            [d[pair[0]].append(r) for r in pair[1]]
        else:
            d[pair[0]] = pair[1]

    for rl in d.values():
        for r in rl:
            region_count += 1 

    print("There are {} regions of interest".format(region_count))

    return d

def convertToMaskRCNN(regionImageData: dict):
    
    # apparently zooniverse allowed people to annotate beyond the actual image dimensions
    maxWidth = 999

    # the actual JSON
    regionDataFormatted = dict()

    for img,regions in regionImageData.items():

        regionDataFormatted[img] = dict()

        regionValue = dict() # the region is itself a dictionary
        for i in range(len(regions)):

            someD = dict()

            # apparently zooniverse allowed people to annotate beyond the actual image width
            x1 = max(1, regions[i][0])
            x2 = min(x1 + regions[i][2], maxWidth)

            y1 = regions[i][1]
            y2 = y1 + regions[i][3]

            # four (x,y) points are needed to create a bounding box
            someD["shape_attributes"] = {"name" : "polygon", "all_points_x": [x1,x2,x2,x1], "all_points_y": [y1,y1,y2,y2]}

            regionValue[str(i)] = someD

        regionDataFormatted[img]["filename"] = img
        regionDataFormatted[img]["regions"] = regionValue

    return regionDataFormatted

regionData = extractROIs(CSV_PATH)

regionDataFormatted = convertToMaskRCNN(regionData)

with open('data.json', 'w') as dataFile:
    json.dump(regionDataFormatted, dataFile)


print(regionDataFormatted)

# to see a text file of the json
# with open('formattedData.txt', 'w') as f:
#     for item in regionDataFormatted.items():
#         f.write("{}\n".format(item))