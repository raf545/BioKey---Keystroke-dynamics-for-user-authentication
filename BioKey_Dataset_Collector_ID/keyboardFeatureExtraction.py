
from cProfile import label
from tkinter import Y
from pynput import keyboard
import numpy as np
from time import time
from database import DataBaseConnector
from PyQt6 import QtCore, QtGui, QtWidgets

class keyboardFeatureExtraction(object):

    def __init__(self) -> None:
        self.dwell = []                   #The list of key dwell times 
        self.startTimes = np.zeros(254)   #Saves the time in witch a key was pressed
        self.startTyping = 0              #strat time
        self.DownDown = []
        self.UpDown = [] 
        self.lastKeyEnterdTime = 0        #a variable used to caclulate the duration between key strokes
        self.virtualKeysID = []           #Contains the key char that was stroked for exsample if k was pressed 'k' will be added
        self.qui = None
        self.charCount = 150
        
    def setQui(self,qui): #save the ui window instance 
        self.qui = qui
    
    def setEmail(self,email): #set a email
        self.email = email
    

    def on_press(self,key):
        #This function take place every key press
        currTime = time() 

        if self.startTyping == 0:
            self.startTyping = currTime

        if self.lastKeyEnterdTime != 0:
            if hasattr(key, 'vk'): #Check if a key has a virtual key attribute
                if self.startTimes[key.vk] == 0: #Calculate the DownDown time and append it to the list
                    self.DownDown.append(currTime - self.lastKeyEnterdTime)
            elif self.startTimes[key.value.vk] == 0:
                self.DownDown.append(currTime - self.lastKeyEnterdTime)
                
        self.lastKeyEnterdTime = currTime #Save the time for a keypress
        
        if hasattr(key, 'vk'):
            if self.startTimes[key.vk] == 0:
                self.startTimes[key.vk] = currTime
                self.virtualKeysID.append(key.vk)

        else:
            if self.startTimes[key.value.vk] == 0:
                self.startTimes[key.value.vk] = currTime 
                self.virtualKeysID.append(key.value.vk)
        print(key,end='')
        
        
    def on_release(self, key):
        currTime = time()
        if self.charCount > 0 and self.charCount <= 150:
            self.charCount -= 1
        
        if hasattr(key, 'vk'):
            start = self.startTimes[key.vk]
            self.startTimes[key.vk] = 0
            
        else: 
            start = self.startTimes[key.value.vk]
            self.startTimes[key.value.vk] = 0
        self.dwell.append(currTime - start)
        
        if key == keyboard.Key.backspace:
            if len(self.qui.Q1TextInputCube.toPlainText()) > 150:
                self.charCount = 0
            else:
                self.charCount = 150 - len(self.qui.Q1TextInputCube.toPlainText())
                
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        self.qui.setCountLable(self.charCount)
    
    def preProcessing(self):
        dwell = np.array(self.dwell)
        DownDown = np.array(self.DownDown)
        UpDown = DownDown - dwell[:len(dwell)-1]
        i = 0

        finalVec = []
            
        for i in range(len(dwell)-1):
            inputVector = (self.virtualKeysID[i],self.virtualKeysID[i+1],dwell[i],dwell[i+1],DownDown[i],UpDown[i])
            finalVec.append(inputVector)
        
        DataBaseConnector._instance.insertInputData(email=self.email, input=str(finalVec))

    