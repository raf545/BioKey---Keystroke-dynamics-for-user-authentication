from mimetypes import init
import re   
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
class Helper():

    def checkEmail(email):   
        regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if(re.search(regex,email)):
            return True 
        else:   
            return False
    
    def checkId(id):
        if len(id)<9:
            return False
        else:
            try:
                intId = int(id)
            except ValueError:
                return False
            
        sum = 0
        for i in range(9):
            if i % 2 == 0:
                mul = 1
            else:
                mul = 2
            ans =  int(id[i]) * mul
            if ans >= 10:
                ahadot = int(int(ans) % 10)
                asarot = int(int(ans) / 10)
                ans = 0
                ans = ans + ahadot + asarot
            sum = sum + ans
        return sum % 10 == 0  
        # sum = int(id[0])*1 + int(id[1])*2 + int(id[2])*1 + int(id[3])*2 + int(id[4])*1 + int(id[5])*2 + int(id[6])*1 + int(id[7])*2 + int(id[8])*1
        # if (int(id[8]) == 0):
        #     mod = 0
        # else:
        #     mod = 9 - int(id[8])
        # if (sum % 10 == mod):
        #     return True
        # else:
        #     return False


    
    def popupWinError(msg):
        msgBox = QMessageBox()
        msgBox.setText(msg)
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Close)
        
        returnValue = msgBox.exec()


    def checkTextField(typing):
        if len(typing) < 150:
            return False
        else:
            return True