from random import Random, shuffle
import json
import math

REGIONS = 4143
SEED = 42


with open('data.json', 'r') as dataFile:
    data = json.load(dataFile)

    buff = list(data.items())

    #print(data)
    Random(SEED).shuffle(buff)

    trainData = []
    valData = []
    testData = []

    idx = 0

    trainDataSize = math.ceil(0.7 * REGIONS)
    valDataSize = math.ceil(0.15 * REGIONS)

    trainCount = 0
    valCount = 0

    while trainCount < trainDataSize:
        trainData.append(buff[idx])
        trainCount += len(buff[idx][1]['regions'])
        idx += 1
        
    while valCount < valDataSize:
        valData.append(buff[idx])
        valCount += len(buff[idx][1]['regions'])
        idx += 1

    testData = buff[idx:]
        
    print(len(trainData))
    print(len(valData))
    print(len(testData))

    trainData = dict(trainData)
    valData = dict(valData)
    testData = dict(testData)

    print(trainData)

    with open('train_via_region_data.json', 'w') as trainFile:
        json.dump(trainData, trainFile)

    with open('val_via_region_data.json', 'w') as valFile:
        json.dump(valData, valFile)

    with open('test_via_region_data.json', 'w') as testFile:
        json.dump(testData, testFile)