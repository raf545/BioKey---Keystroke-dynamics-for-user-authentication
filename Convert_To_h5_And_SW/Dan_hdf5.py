from sklearn.utils import shuffle
import numpy as np
import os
import ast
import h5py
import random

#The diractory of the Dataset on the computer
a_directory_test = "/Users/rafaelelkoby/Downloads/Data_convertion_script/Converted_S0/Converted_baseline"
windowSize = 30


#Final data and lables data.
train_data = np.array([])
train_labels = np.array([])
sliding_window_data = np.array([])

#This function reads the data from a given file and filepath. removes the - [] from 
#the start and the end of the file data string, then converts it to a list of tupels.
def file_command(filepath,filename):
    places = []

    # open file and read the content in a list
    with open(filepath, 'r') as filehandle:
        filecontents = filehandle.readlines()
        for line in filecontents:
            line.removeprefix('[')
            line.removesuffix(']')
            x = ast.literal_eval(line)       
    return x


def dataTrans(a_directory):
    global train_data
    global train_labels
    global sliding_window_data

    for i,filename in enumerate(os.listdir(a_directory)):
        if i==150:
            break

        #check only the txt files
        if filename.find(".txt") != -1:
            filepath = os.path.join(a_directory, filename)
            print(filename)
            #Taking the first 3 chars to know the id
            lable = int(filename[0:3])
            #Getting the file content as a list of Tupels.
            new_train_data = np.array(file_command(filepath,filename))
            #Normalize the values of the keycode id of every tuple
            for j in range(0,len(new_train_data)):
                new_train_data[j][0] = new_train_data[j][0]/254
                new_train_data[j][1] = new_train_data[j][1]/254

            #Taking a reletive data portion 
            x = random.randint(0, new_train_data.shape[0] - 81)
            new_train_data = new_train_data[x:x+80]
            #Sliding Window on given input data
            for k in range(new_train_data.shape[0] - windowSize):
                sliding_window_data = np.append(sliding_window_data , new_train_data[k:k+windowSize])

            #Create labels
            temp = np.empty(int(new_train_data.shape[0] - windowSize))
            temp.fill(0)
            train_labels = np.append(train_labels , temp)
                
dataTrans("/Volumes/GoogleDrive-112371676829911023923/My Drive/BioKey/Data_convertion_script/Converted_S0/Converted_baseline")
dataTrans("/Volumes/GoogleDrive-112371676829911023923/My Drive/BioKey/Data_convertion_script/Converted_S1/Converted_Baseline")
dataTrans("/Volumes/GoogleDrive-112371676829911023923/My Drive/BioKey/Data_convertion_script/Converted_S2/Converted_Baseline")

#dan data
dp = '/Volumes/GoogleDrive-112371676829911023923/My Drive/BioKey/Data_convertion_script/Dan Data'
dv = np.array([])
for i,filename in enumerate(os.listdir(dp)):
    if filename.find(".txt") != -1:
        filepath = os.path.join(dp, filename)
        dv = np.append(dv,np.loadtxt(filepath))
dv = dv.reshape(int(dv.shape[0]/6),6)

for j in range(0,len(dv)):
    dv[j][0] = dv[j][0]/254
    dv[j][1] = dv[j][1]/254

#Sliding Window on given input data
for k in range(dv.shape[0] - windowSize):
    sliding_window_data = np.append(sliding_window_data , dv[k:k+windowSize])

temp = np.empty(dv.shape[0] - windowSize)
temp.fill(1)
train_labels = np.append(train_labels , temp)

train_labels = train_labels.reshape(int(train_labels.shape[0]),1)
sliding_window_data = sliding_window_data.reshape(int(train_labels.shape[0]),windowSize,6)
sliding_window_data,train_labels = shuffle(sliding_window_data,train_labels)

print(sliding_window_data.shape)


with h5py.File('Rand_Dan_WS30.h5','w') as hdf: 
  hdf.create_dataset('train_data',data = sliding_window_data)
  hdf.create_dataset('train_labels',data = train_labels)
