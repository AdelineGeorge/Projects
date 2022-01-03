import pickle
import json
import os
path = 'C:/Users/Sherya Sathyan/Downloads/r/'
filelist = os.listdir(path)

for i in filelist:
    car_pickle = open (path+i, "rb")
    car_contents = pickle.load(car_pickle)
    data = car_contents.to_json(orient='index')
    jsonFile = open('C:/Users/Sherya Sathyan/Downloads/json/test.json', 'a')
    jsonFile.write(data)
    jsonFile.close()


  
