import numpy as np
from sklearn.metrics import roc_curve
import os
import matplotlib.pyplot as plt
import numpy as np

a_directory = "/Volumes/GoogleDrive-112371676829911023923/My Drive/BioKey/Testing system/Experiment results"
all_data = np.array([])
all_labels = np.array([])
Dan_data = np.array([])
Dan_labels = np.array([])
not_dan_data = np.array([])
not_dan_labels = np.array([])
frr = []
far = []
#Get presentage of FAR
def FARammount(data):
    numFAR = 0
    for pred in data:
        if pred > 0.5:
            numFAR += 1
    return (numFAR/len(data))* 100
#Get presentage of FAR for all thresholds
def calcFAR():
    global far
    for i in range(100):
            num = 0

            for x in not_dan_data:
                    if (x*100)>i:
                            num+=1
            #print(i,num)
            far.append(num)
    far = np.array(far)
#Get presentage of FRR
def FRRammount(data):
    numFRR = 0
    for pred in data:
        if pred < 0.7:
            numFRR += 1
    return (numFRR/len(data))* 100
#Get presentage of FRR for all thresholds
def calcFRR():
    global frr
    for i in range(100):
            num = 0

            for x in Dan_data:
                    if (x*100)<i:
                            num+=1
            #print(i,num)
            frr.append(num)
    frr = np.array(frr)

def compute_eer(label, pred, positive_label=1):
    # all fpr, tpr, fnr, fnr, threshold are lists (in the format of np.array)
    fpr, tpr, threshold = roc_curve(label, pred, pos_label=1)
    fnr = 1 - tpr

    # the threshold of fnr == fpr
    eer_threshold = threshold[np.nanargmin(np.absolute((fnr - fpr)))]

    # theoretically eer from fpr and eer from fnr should be identical but they can be slightly differ in reality
    eer_1 = fpr[np.nanargmin(np.absolute((fnr - fpr)))]
    eer_2 = fnr[np.nanargmin(np.absolute((fnr - fpr)))]

    # return the mean of eer from fpr and from fnr
    eer = (eer_1 + eer_2) / 2
    return eer*100

#Iterate over all the files in the directory, append it and create corresponding labels
for filename in os.listdir(a_directory):
    data = np.array([])
    labels = np.array([])
    if filename.find(".txt") != -1:
        filepath = os.path.join(a_directory, filename)
        data = np.loadtxt(filepath)
        labels = np.empty(len(data))
        if filename == "Dan.txt":
            labels.fill(1)
            Dan_data = data
            Dan_labels = labels
        else:
            labels.fill(0)
            not_dan_data = np.append(not_dan_data, data)
            not_dan_labels = np.append(not_dan_labels, labels)
        all_data = np.append(all_data, data)
        all_labels = np.append(all_labels, labels)
#Print precentages
eer = compute_eer(all_labels, all_data)
print('The equal error rate is {:.3f}'.format(eer))
print("FAR not dan- "+ str(FARammount(not_dan_data)))
print("FRR dan- "+ str(FRRammount(Dan_data)))

threshold = list(range(0, 100))
fig, ax = plt.subplots()

calcFAR()
calcFRR()

#plot data
ax.plot(threshold, far, 'r--', label='FAR')
ax.plot(threshold, frr, 'g--', label='FRR')
plt.xlabel('Threshold')
plt.plot(15,eer,'ro', label='EER') 


legend = ax.legend(loc='upper right', shadow=True, fontsize='x-large')

plt.show()