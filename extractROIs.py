### To be used on the stripped version of the csv file generated from zooniverse

import pandas as pd
import json

CSV_PATH = '/Users/silver/Desktop/buildUCLA/stripped-book-annotation-classification-classifications-11June2018.csv'

# ASSUMES FILES ARE .PNG FORMAT
META_DATA_PATH = '/Users/silver/Desktop/buildUCLA/phase2/annotations-computervision/books meta data.csv'

# WARNING CSV file is inconsistent with the key identifier for the key names. For now, we will only retain the data that uses 'filename' as the key to retrieve the file name
def extractROIs(csv_file_path):
	assert csv_file_path
	df = pd.read_csv(csv_file_path, usecols=['annotations', 'subject_data','subject_ids'])

	# need to add this bit to map file names to the randomized IDs
	df_meta = pd.read_csv(META_DATA_PATH, usecols=['ID','File Name'])
	name2id = dict()
	for index, row in df_meta.iterrows():
		name2id[row[1].replace('.png','.jpg')] = row[0]

	fileNames = []
	coordinates = []

	# gets all fileNames of images in rows that use 'filename' as the key
	for index, row in df.iterrows():

		s_id = str(row['subject_ids'])

		s_data = json.loads(row['subject_data'])

		try: # if this succeeds, then we can retrieve its annotations as well
			
			fn = s_data[s_id]['filename']

			print(name2id[fn])

			fileNames.append(name2id[s_data[s_id]['filename']])
			
			tasks = json.loads(df.iloc[index]['annotations'])

			imageCoordinates = []

			for t in tasks:

				if t['task'] == 'T1':
					listOfCoordinates = t['value']

					for coord in listOfCoordinates:
						formattedCoord = coord['x'], coord['y'], coord['width'], coord['height']
						imageCoordinates.append(formattedCoord)

			coordinates.append(imageCoordinates)
		except:
			continue

	return zip(fileNames,coordinates)

regionData = extractROIs(CSV_PATH)

for rd in regionData:
	print(rd)