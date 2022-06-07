from pip import main
import KeyMap
import os

'''
Description: This conversion script convert the data we got from buffalo to our format.

        A KeyDown 63578429792961
        A KeyUp 63578429793054
        ...
        ...
        ...
        M KeyDown 63578429793257
        M KeyUp 63578429793382
                |
                |
                |
                V
(ID[1] | ID[2] | Dwell[1] | Dwell[2] | UD[1][2] | DD[1][2])

Output: A file containing the converted data

Algorithm: We run on the data and search a key that is pressed down and then released and calculate the dwell time(keyUp - keyDown).
           And between adjecent keyes we calculate the downDown(keyDown1 - keyDown2) and downUp(keyDown - keyUp),we do that for evrey key in the dataset.
'''

a_directory = "/Users/rafaelelkoby/Desktop/UB_keystroke_dataset/s2/rotation" #input directory
out_directory = "/Users/rafaelelkoby/Desktop/College/Semester 8/Capstopne project phase B/DataConvertionScript/Converted_S2/Converted_Rotation" #output directory for saving the converted files

def file_command(filepath,filename):
    
    up = []
    down = []
    inputVector = []

    f = open(filepath, "r")
    content = f.read()
    newcontent = content.split("\n") # split the data into a list that every cell in the list is a row in the dataset
    x = [] 
    for i in newcontent:
        x.append(i.split(" "))
    x.remove(x[len(x)-1])

    for row in range(len(x)-1):
        for row2 in range(row+1,len(x)-1):
            if x[row2][0] == x[row][0] and x[row][1] == 'KeyDown' and x[row2][1] == 'KeyUp':
                if str(x[row][0]).find(',') != -1:
                    x[row][0] = str(x[row][0]).replace(',', '')
                if str(x[row2][0]).find(',') != -1:
                    x[row2][0] = str(x[row2][0]).replace(',', '')
                downcon = [KeyMap.virtualKeyMap[str(x[row][0]).upper()],x[row][1],int(x[row][2])] #check the ID of the key in the keyMap file
                down.append(downcon)
                
                upcon = [KeyMap.virtualKeyMap[str(x[row2][0]).upper()],x[row2][1],int(x[row2][2])] #check the ID of the key in the keyMap file
                up.append(upcon)
                break

    for i in range(len(up)-2):
        k1up = up[i]
        k1down = down[i]
        k2up = up[i+1]
        k2down = down[i+1]

        #Calculate the times of every feature and save it to the input vactor
        inputVector.append((k1up[0],k2up[0],(k1up[2] - k1down[2])/1000,(k2up[2] - k2down[2])/1000,(k2down[2] - k1down[2])/1000,(k2down[2] - k1up[2])/1000)) 

    outputFile = open(out_directory+"/"+filename, "w")
    outputFile.write(str(inputVector))

#For every file in the input directory call the conversion function and save the converted file in the out-directory
for filename in os.listdir(a_directory):
    if filename.find(".txt") != -1 and filename not in os.listdir(out_directory):
        filepath = os.path.join(a_directory, filename)
        print(filepath)
        file_command(filepath,filename)