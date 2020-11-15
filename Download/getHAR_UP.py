"""
Author: Tuan Anh Le - @mausLe
"""

import numpy as np
import pandas as pd

with open("C:\Thesis\Monitor\Fall detection\Codes\stuff\crawling data\HAR-UP.html", "r", encoding="utf-8") as f:
    text = f.readlines()


# Remove lines do not contain subject and download link
for i in range(len(text) - 1, -1, -1):
    if (text[i].find("drive.google.com/a/up.edu.mx") != -1) or (text[i].find("&lt;h5&gt;Subject") != -1):
        continue
    else:
        del text[i]


# Get the subject name 
# '\t\t\t\t&lt;h5&gt;Subject1Activity1Trial1&lt;/h5&gt;\n' -> Subject1Activity1Trial1

for i in range(len(text) - 1, -1, -1):
    if (text[i].find("Activity") != -1):

        text[i] = text[i].split(";")
        for item in text[i]:
            if item.find("Activity") != -1:
                
                text[i] = item.replace("&lt", "")
                break
    
    
    if (text[i].find("drive.google.com/a/up.edu.mx") != -1):
        a = text[i].split(";")

        del a[6:]
        del a[4]

        del a[1]
        del a[0]

        a[2] = a[2].replace("&amp", "")
        a[2] = a[2].replace("&lt", "")
        a[1] = a[1].replace("&quot", "")
        a[0] = a[0].replace("&amp", "")

        text[i] = a

subPos = [] 
for i in range(len(text)):
    if isinstance(text[i], str):
        subPos.append(i)

HAR_UP = []
# Append the video names and the downloads source into a list
for i in range(len(subPos) - 1):
    temp = []
    temp.append(text[subPos[i]])

    temp.append(text[subPos[i] + 1 : subPos[i + 1]] )

    HAR_UP.append(temp)


temp = []
temp.append(text[subPos[i]])
temp.append(text[subPos[-1] + 1: ] )
HAR_UP.append(temp)

# With the Subject6Activity10Trial2
# It was missing 'Camera Resized OF', 'Camera OF Features1', 'Camera OF Features2', 'Camera OF Features3'
# the others is still ok, so I add "nothing" to pass the error 
# and keep the remaining data
s = ["nothing", "nothing","nothing"]
for i in range(4):
    HAR_UP[193][1].append(s)

# remove Trials that do not contain anything

del HAR_UP[263] # Subject8Activity11Trial3
del HAR_UP[262] # Subject8Activity11Trial2

download = []
video = []
for item in HAR_UP:
    try:
        video.append(item[0])
        download.append(item[1])
    except IndexError:
       pass
inputArray = np.array(download)

df = pd.DataFrame(inputArray[:, :, 0], index= video,columns=inputArray[0, :, -1])
df.to_csv("HAR_UP_HFD_dataset.csv", header=True)

